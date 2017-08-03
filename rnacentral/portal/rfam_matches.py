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

This module contains code to detect certain types of problems with Rfam matches
to sequences. That is it can find if the sequence and Rfam domain conflict, or
if the sequence is only a partial sequence
"""

import json

import attr
from attr.validators import instance_of as is_a


@attr.s()
class RfamMatchStatus(object):
    """
    This represents implied problems from a match between an Rfam family and an
    Rna sequence. Problems are detected by various objects and this simply
    records which ones have found issues as well as some data about the issues.
    This serves as a simple way to organize many possible issues that could be
    detected.
    """

    has_issue = attr.ib(validator=is_a(bool))
    upi = attr.ib(validator=is_a(basestring))
    taxid = attr.ib()
    finders = attr.ib(validator=is_a(list))
    messages = attr.ib(validator=is_a(list))

    @classmethod
    def with_issue(cls, upi, taxid, finder, msg):
        """
        Create a new instance that indicates that the given finder has found an
        issue specified in the given message.
        """
        return cls(has_issue=True, upi=upi, taxid=taxid, finders=[finder], messages=[msg])

    @classmethod
    def no_issues(cls, upi, taxid):
        """
        Create a new instance that indicates there are no issues.
        """
        return cls(has_issue=False, upi=upi, taxid=taxid, finders=[], messages=[])

    @property
    def names(self):
        """
        Get the names of all finders that have found issues.
        """
        return sorted([finder.name for finder in self.finders])

    def merge(self, status):
        """
        Merge the given status with this one. This will update the issues found
        if any.
        """
        if status.upi != self.upi and self.taxid == status.taxid:
            raise ValueError("Can only merge MatchStatus from the same RNA.")

        self.finders.extend(status.finders)
        self.messages.extend(status.messages)
        self.has_issue = (self.has_issue or status.has_issue)
        return self

    def as_simple_data(self):
        """
        Create a simplified dict representation of this data. This is useful
        for storage.
        """
        return {
            'has_issue': self.has_issue,
            'problems': [{'name': n} for n in self.names],
        }

    def as_json(self):
        """
        Create a JSON representation of the simplified data.
        """
        return json.dumps(self.as_simple_data())


class DomainProblem(object):
    """
    This detects if there is a mismatch between the domains of the matched
    models and the sequence that has been run. For example if a bacterial model
    only matches a mouse sequence then there is some sort of problem, likely
    contamination, with the sequence.
    """
    name = 'domain_conflict'

    def message(self, model, rna, taxid=None):
        """
        Get a message that indicates a problem.
        """

        differing = rna.get_domains() - set([model.domain])
        differing = ', '.join(sorted(differing))
        return 'This %s sequence matches a %s Rfam model' % (
            differing,
            model.domain
        )

    def __call__(self, rna, taxid=None):
        hits = rna.get_rfam_hits()
        if not hits or len(hits) > 1:
            return RfamMatchStatus.no_issues(rna.upi, taxid)

        model = hits[0].rfam_model
        found = model.domain
        if not found:
            return RfamMatchStatus.no_issues(rna.upi, taxid)
        if set([found]) != rna.get_domains(taxid=taxid):
            msg = self.message(model, rna)
            return RfamMatchStatus.with_issue(rna.upi, taxid, self, msg)
        return RfamMatchStatus.no_issues(rna.upi, taxid)


class IncompleteSequence(object):
    """
    This checks if a sequence is considered incomplete according to it's
    Rfam match. This is detected if the at least 90% sequence matches the
    model but less 50% of the model is matched by the sequence. In
    addition, we require that it only have one match. This will only work for
    hits that are part of a selected set of families.
    """
    name = 'incomplete_sequence'

    def message(self, hit):
        """
        Get a message that indicates a problem.
        """

        return ('This sequence appears to be an incomplete instance of the %s'
                ' model' %
                hit.rfam_model.long_name)

    def allowed_families(self):
        """
        Get the set of families we will check for incomplete sequences. We
        don't want to do all families yet, as we aren't sure if this will
        be too senestive. The selected families are well known for having
        partial sequences.
        """

        return set([
            'RF00001',  # 5S ribosomal RNA
            'RF00002',  # 5.8S ribosomal RNA
            'RF00005',  # tRNA
            'RF00177',  # Bacterial small subunit ribosomal RNA
            'RF01959',  # Archaeal small subunit ribosomal RNA
            'RF01960',  # Eukaryotic small subunit ribosomal RNA
            'RF02540',  # Archaeal large subunit ribosomal RNA
            'RF02541',  # Bacterial large subunit ribosomal RNA
            'RF02542',  # Microsporidia small subunit ribosomal RNA
            'RF02543',  # Eukaryotic large subunit ribosomal RNA
        ])

    def __call__(self, rna, taxid=None):
        hits = rna.get_rfam_hits()
        if len(hits) != 1:
            return RfamMatchStatus.no_issues(rna.upi, taxid)

        if hits[0].rfam_model_id not in self.allowed_families():
            return RfamMatchStatus.no_issues(rna.upi, taxid)

        if hits[0].model_completeness <= 0.5 and \
                hits[0].sequence_completness >= 0.9:
            msg = self.message(hits[0])
            return RfamMatchStatus.with_issue(rna.upi, taxid, self, msg)
        return RfamMatchStatus.no_issues(rna.upi, taxid)


class RnaTypeConflict(object):
    """
    This will detect if the sequence has a conflicting RNA type from the Rfam
    family that it matches. This is likely a sign that the sequence has been
    mis-annotated somehow and care should be taken when working with it.
    """
    name = 'rna_type_conflict'

    def message(self, model, rna, **kwargs):
        """
        Get a message that indicates a problem.
        """
        return 'This %s sequence matches an Rfam family of %s sequences' % \
            (rna.get_rna_type(), model.rna_type)

    def __call__(self, rna, taxid=None):
        return RfamMatchStatus.no_issues(rna.upi, taxid)


@attr.s()
class UnmodelledRnaType(object):
    """
    Check if this Rna object should match at least one match to an Rfam
    family. This is done by seeing if it is not an lncRNA or piRNA as those
    are not modeled by Rfam.

    :returns bool: True if this Rna should have an Rfam match.
    """
    name = 'unexpected_match'

    def message(self, rna):
        """
        Get a message that indicates a problem.
        """
        if rna.get_rna_type() == 'lncRNA':
            return ("This sequence is not expected to match an Rfam model "
                    "because Rfam does not model full length lncRNA's, but"
                    " matches:")

        if rna.get_rna_type == 'piRNA':
            return ("This sequence is not expected to match an Rfam match a "
                    "model because Rfam does not model piRNA's, but matches:")

        raise ValueError("Impossible state")

    def __call__(self, rna, taxid=None):
        if rna.get_rna_type() in set(['lncRNA', 'piRNA']) and \
                rna.get_rfam_hits():
            message = self.message(rna)
            return RfamMatchStatus.with_issue(rna.upi, taxid, self, message)
        return RfamMatchStatus.no_issues(rna.upi, taxid)


def check_issues(rna, taxid=None):
    finders = [
            UnmodelledRnaType(),
            DomainProblem(),
            IncompleteSequence(),
            RnaTypeConflict(),
        ]

    issue = RfamMatchStatus.no_issues(rna.upi, taxid)
    for finder in finders:
        issue.merge(finder(rna, taxid=taxid))
    return issue
