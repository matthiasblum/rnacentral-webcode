"""
Copyright [2009-2017] EMBL-European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import math
import re
import requests
import six

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.template import TemplateDoesNotExist
from django.views.decorators.cache import cache_page, never_cache
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from rest_framework.response import Response
from rest_framework.views import APIView

from portal.config.expert_databases import expert_dbs
from portal.forms import ContactForm
from portal.models import Rna, Database, Release, Xref, EnsemblAssembly
from portal.models.database_stats import DatabaseStats
from portal.models.rna_precomputed import RnaPrecomputed

CACHE_TIMEOUT = 60 * 60 * 24 * 1 # per-view cache timeout in seconds
XREF_PAGE_SIZE = 1000

########################
# Function-based views #
########################

@cache_page(CACHE_TIMEOUT)
def get_sequence_lineage(request, upi):
    """
    Internal API.
    Get the lineage for an RNA sequence based on the
    classifications from all database cross-references.
    """
    try:
        queryset = Xref.objects.filter(upi=upi).select_related('accession')
        results = queryset.filter(deleted='N')
        if not results.exists():
            results = queryset
        json_lineage_tree = _get_json_lineage_tree(results.iterator())
    except Rna.DoesNotExist:
        raise Http404
    return HttpResponse(json_lineage_tree, content_type="application/json")


@cache_page(60)
def homepage(request):
    """RNAcentral homepage."""
    context = {
        'databases': list(Database.objects.filter(alive='Y').order_by('?').all()),
        'blog_url': settings.RELEASE_ANNOUNCEMENT_URL,
    }
    return render(request, 'portal/homepage.html', {'context': context})


@cache_page(CACHE_TIMEOUT)
def expert_databases_view(request):
    """List of RNAcentral expert databases."""
    context = {
        'expert_dbs': sorted(expert_dbs, key=lambda x: x['name'].lower()),
        'num_imported': len([x for x in expert_dbs if x['imported']]),
    }
    return render(request, 'portal/expert-databases.html', {'context': context})


@cache_page(CACHE_TIMEOUT)
def rna_view_redirect(request, upi, taxid):
    """Redirect from urs_taxid to urs/taxid."""
    return redirect('unique-rna-sequence', upi=upi, taxid=taxid)


@cache_page(CACHE_TIMEOUT)
def rna_view(request, upi, taxid=None):
    """
    Unique RNAcentral Sequence view.
    Display all annotations or customize the page using the taxid (optional).
    """
    # get Rna or die
    upi = upi.upper()
    try:
        rna = Rna.objects.get(upi=upi)
    except Rna.DoesNotExist:
        raise Http404

    # if taxid is given, but the RNA does not have annotations for this taxid, redirect to an error page
    if taxid and not RnaPrecomputed.objects.filter(upi=upi, taxid=taxid).exists():
        response = redirect('unique-rna-sequence', upi=upi)
        response['Location'] += '?taxid-not-found={taxid}'.format(taxid=taxid)
        return response

    taxid_filtering = True if taxid else False

    symbol_counts = rna.count_symbols()
    non_canonical_base_counts = {key: symbol_counts[key] for key in symbol_counts if key not in ['A', 'U', 'G', 'C']}

    context = {
        'symbol_counts': symbol_counts,
        'non_canonical_base_counts': non_canonical_base_counts,
        'taxid': taxid,
        'taxid_filtering': taxid_filtering,
        'taxid_not_found': request.GET.get('taxid-not-found', ''),
        'description': rna.get_description(taxid) if taxid_filtering else rna.get_description(),
        'distinct_databases': rna.get_distinct_database_names(taxid),
        'publications': rna.get_publications(taxid) if taxid_filtering else rna.get_publications(),
        'tab': request.GET.get('tab', ''),
        'xref_pages': six.moves.range(1, int(math.ceil(rna.count_xrefs()/float(XREF_PAGE_SIZE))) + 1),
        'xref_page_size': XREF_PAGE_SIZE,
        'xref_page_num': int(request.GET.get('xref-page')) if request.GET.get('xref-page') else 1,
        'xrefs_count': rna.count_xrefs(taxid) if taxid_filtering else rna.count_xrefs(),
        'precomputed': RnaPrecomputed.objects.filter(upi=upi, taxid=taxid).first(),
        'rfam_status': rna.get_rfam_status(taxid=taxid),
    }

    return render(request, 'portal/sequence.html', {'rna': rna, 'context': context})


@cache_page(CACHE_TIMEOUT)
def expert_database_view(request, expert_db_name):
    """Expert database view."""
    def _normalize_expert_db_name(expert_db_name):
        """Expert_db_name should match RNACEN.RNC_DATABASE.DESCR."""
        dbs = Database.objects.values_list('descr', flat=True)
        dbs_coming_soon = ()
        if re.match('tmrna-website', expert_db_name, flags=re.IGNORECASE):
            expert_db_name = 'TMRNA_WEB'
        else:
            expert_db_name = expert_db_name.upper()
        if expert_db_name in dbs:
            return expert_db_name
        elif expert_db_name in dbs_coming_soon:
            return 'coming_soon'
        else:
            return False

    expert_db_name = _normalize_expert_db_name(expert_db_name)
    if expert_db_name and expert_db_name != 'coming_soon':
        expert_db = Database.objects.get(descr=expert_db_name)
        expert_db_stats = DatabaseStats.objects.get(database=expert_db_name)
        if expert_db_name == 'LNCRNADB':
            lncrnadb = Rna.objects.filter(xrefs__accession__database=expert_db_name).\
                                   order_by('-length').\
                                   all()
        else:
            lncrnadb = []
        return render_to_response('portal/expert-database.html', {
            'expert_db': expert_db,
            'expert_db_stats': expert_db_stats,
            'lncrnadb': lncrnadb,
            'no_sunburst': ['ENA', 'RFAM', 'SILVA', 'GREENGENES'],
        })
    elif expert_db_name == 'coming_soon':
        return render_to_response('portal/coming-soon.html')
    else:
        raise Http404()


@never_cache
def website_status_view(request):
    """
    This view will be monitored by Nagios for the presence
    of string "All systems operational".
    """
    def _is_database_up():
        try:
            rna = Rna.objects.all()[0]
            return True
        except:
            return False

    def _is_api_up():
        return True

    def _is_search_up():
        return True

    context = dict()
    context['is_database_up'] = _is_database_up()
    context['is_api_up'] = _is_api_up()
    context['is_search_up'] = _is_search_up()
    context['overall_status'] = context['is_database_up'] and context['is_api_up'] and context['is_search_up']
    return render_to_response('portal/website-status.html', {'context': context})


@cache_page(CACHE_TIMEOUT)
def ebeye_proxy(request):
    """
    Internal API.
    Get EBeye search URL from the client and send back the results.
    Bypasses EBeye same-origin policy.
    """
    url = request.GET['url']
    try:
        ebeye_response = requests.get(url)
        if ebeye_response.status_code == 200:
            response = HttpResponse(ebeye_response.text)
            return response
        else:
            raise Http404
    except:
        raise Http404

#####################
# Class-based views #
#####################

class StaticView(TemplateView):
    """Render flat pages."""
    def get(self, request, page, *args, **kwargs):
        self.template_name = 'portal/' + page + '.html'
        response = super(StaticView, self).get(request, *args, **kwargs)
        try:
            return response.render()
        except TemplateDoesNotExist:
            raise Http404()


class GenomeBrowserView(TemplateView):
    """Render genome-browser, taking into account start/end locations."""
    def get(self, request, *args, **kwargs):
        self.template_name = 'portal/genome-browser.html'

        # if current location is given in GET parameters - use it; otherwise, use defaults
        if 'species' in request.GET and ('chromosome' in request.GET or 'chr' in request.GET) and 'start' in request.GET and 'end' in request.GET:
            # security-wise it doesn't make sense to validate location:
            # if user tinkers with it, she won't shoot anyone but herself

            # find our genome in taxonomy, replace genome with a dict with taxonomy data
            kwargs['genome'] = request.GET['species']
            if kwargs['genome'] is None:
                raise Http404

            # 'chromosome' takes precedence over 'chr'
            if 'chromosome' in request.GET:
                kwargs['chromosome'] = request.GET['chromosome']
            else:
                kwargs['chromosome'] = request.GET['chr']

            kwargs['start'] = request.GET['start']
            kwargs['end'] = request.GET['end']
        else:
            ensembl_assembly = EnsemblAssembly.objects.get(ensembl_url='homo_sapiens')

            kwargs['genome'] = 'homo_sapiens'
            kwargs['chromosome'] = ensembl_assembly.example_chromosome
            kwargs['start'] = ensembl_assembly.example_start
            kwargs['end'] = ensembl_assembly.example_end

        response = super(GenomeBrowserView, self).get(request, *args, **kwargs)
        try:
            return response.render()
        except TemplateDoesNotExist:
            raise Http404()


class ContactView(FormView):
    """Contact form view."""
    template_name = 'portal/contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if form.send_email():
            return redirect('contact-us-success')
        else:
            return redirect('error')


####################
# Helper functions #
####################


def _get_json_lineage_tree(xrefs):
    """
    Combine lineages from multiple xrefs to produce a single species tree.
    The data are used by the d3 library.
    """

    def get_lineages_and_taxids():
        """Combine the lineages from all accessions in a single list."""
        if isinstance(xrefs, list):
            for xref in xrefs:
                lineages.add(xref[0])
                taxids[xref[0].split('; ')[-1]] = xref[1]
        else:
            for xref in xrefs:
                lineages.add(xref.accession.classification)
                taxids[xref.accession.classification.split('; ')[-1]] = xref.taxid

    def build_nested_dict_helper(path, text, container):
        """Recursive function that builds the nested dictionary."""
        segs = path.split('; ')
        head = segs[0]
        tail = segs[1:]
        if not tail:
            # store how many time the species is seen
            try:
                if head in container:
                    container[head] += 1
                else:
                    container[head] = 1
            except:
                container = {}
                container[head] = 1
        else:
            try:
                if head not in container:
                    container[head] = {}
            except:
                container = {}
                container[head] = 1
            build_nested_dict_helper('; '.join(tail), text, container[head])

    def get_nested_dict(lineages):
        """
        Transform a list like this:
            items = [
                'A; C; X; human',
                'A; C; X; human',
                'B; D; Y; mouse',
                'B; D; Z; rat',
                'B; D; Z; rat',
            ]
        into a nested dictionary like this:
            {'root': {'A': {'C': {'X': {'human': 2}}}, 'B': {'D': {'Y': {'mouse': 1}, 'Z': {'rat': 2}}}}}
        """
        container = {}
        for lineage in lineages:
            build_nested_dict_helper(lineage, lineage, container)
        return container

    def get_nested_tree(data, container):
        """
        Transform a nested dictionary like this:
            {'root': {'A': {'C': {'X': {'human': 2}}}, 'B': {'D': {'Y': {'mouse': 1}, 'Z': {'rat': 2}}}}}
        into a json file like this (fragment shown):
            {"name":"A","children":[{"name":"C","children":[{"name":"X","children":[{"name":"human","size":2}]}]}]}
        """
        if not container:
            container = {
                "name": 'All',
                "children": []
            }
        for name, children in six.iteritems(data):
            if isinstance(children, int):
                container['children'].append({
                    "name": name,
                    "size": children,
                    "taxid": taxids[name],
                })
            else:
                container['children'].append({
                    "name": name,
                    "children": []
                })
                get_nested_tree(children, container['children'][-1])
        return container

    lineages = set()
    taxids = dict()
    get_lineages_and_taxids()
    nodes = get_nested_dict(lineages)
    json_lineage_tree = get_nested_tree(nodes, {})
    return json.dumps(json_lineage_tree)
