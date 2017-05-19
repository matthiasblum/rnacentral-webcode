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


def location_from_ensembl(string):
    """
    This will parse an Ensembl location string of the form 'MT:7721-10971' into
    a dict specifying the start and endpoints of that location
    """

    chromosome, endpoints = string.split(':', 1)
    endpoints = endpoints.replace(',', '').split('-')
    start, stop = [int(point.strip()) for point in endpoints]
    return {'chromosome': chromosome, 'start': start, 'end': stop}


"""
Supported genomes.
"""
genomes = [
    # Ensembl
    {
        'species': 'Homo sapiens',
        'synonyms': ['human'],
        'assembly': 'GRCh38',
        'assembly_ucsc': 'hg38',
        'taxid': 9606,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 'X',
            'start': 73819307,
            'end': 73856333,
        },
    },
    {
        'species': 'Mus musculus',
        'synonyms': ['mouse'],
        'assembly': 'GRCm38',
        'assembly_ucsc': 'mm10',
        'taxid': 10090,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 1,
            'start': 86351908,
            'end': 86352200,
        },
    },
    {
        'species': 'Danio rerio',
        'synonyms': ['zebrafish'],
        'assembly': 'GRCz10',
        'assembly_ucsc': 'danRer10',
        'taxid': 7955,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 9,
            'start': 7633910,
            'end': 7634210,
        },
    },
    {
        'species': 'Bos taurus',
        'synonyms': ['cow'],
        'assembly': 'UMD3.1',
        'assembly_ucsc': 'bosTau6',
        'taxid': 9913,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 15,
            'start': 82197673,
            'end': 82197837,
        },
    },
    {
        'species': 'Rattus norvegicus',
        'synonyms': ['rat'],
        'assembly': 'Rnor_6.0',
        'assembly_ucsc': 'rn6',
        'taxid': 10116,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 'X',
            'start': 118277628,
            'end': 118277850,
        },
    },
    {
        'species': 'Felis catus',
        'synonyms': ['cat'],
        'assembly': 'Felis_catus_6.2',
        'assembly_ucsc': 'felCat5',
        'taxid': 9685,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 'X',
            'start': 18058223,
            'end': 18058546,
        },
    },
    {
        'species': 'Macaca mulatta',
        'synonyms': ['macaque'],
        'assembly': 'MMUL_1',
        'assembly_ucsc': '', # no matching assembly
        'taxid': 9544,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 1,
            'start': 146238837,
            'end': 146238946,
        },
    },
    {
        'species': 'Pan troglodytes',
        'synonyms': ['chimp'],
        'assembly': 'CHIMP2.1.4',
        'assembly_ucsc': 'panTro4',
        'taxid': 9598,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 11,
            'start': 78369004,
            'end': 78369219,
        },
    },
    {
        'species': 'Canis familiaris',
        'synonyms': ['dog', 'Canis lupus familiaris'],
        'assembly': 'CanFam3.1',
        'assembly_ucsc': 'canFam3',
        'taxid': 9615,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 19,
            'start': 22006909,
            'end': 22007119,
        },
    },
    {
        'species': 'Gallus gallus',
        'synonyms': ['chicken'],
        'assembly': 'Galgal4',
        'assembly_ucsc': 'galGal4',
        'taxid': 9031,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 9,
            'start': 15676031,
            'end': 15676160,
        },
    },
    {
        'species': 'Xenopus tropicalis',
        'synonyms': ['frog'],
        'assembly': 'JGI_4.2',
        'assembly_ucsc': 'xenTro3',
        'taxid': 8364,
        'division': 'Ensembl',
        'example_location': {
            'chromosome': 'NC_006839',
            'start': 11649,
            'end': 11717,
        },
    },
    {'assembly': 'vicPac1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('GeneScaffold_1192:765017-764826'),
     'species': 'Vicugna pacos',
     'synonyms': ['alpaca'],
     'taxid': 30538},
    {'assembly': 'Poecilia_formosa-5.1.2',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('KI520103.1:196751-196536'),
     'species': 'Poecilia formosa',
     'synonyms': ['amazon molly'],
     'taxid': 48698},
    {'assembly': 'AnoCar2.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('2:191625427-191610439'),
     'species': 'Anolis carolinensis',
     'synonyms': ['anole lizard'],
     'taxid': 28377},
    {'assembly': 'Dasnov3.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Dasypus novemcinctus',
     'synonyms': ['armadillo'],
     'taxid': 9361},
    {'assembly': 'OtoGar3',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('GL873949.1:1606-1418'),
     'species': 'Otolemur garnettii',
     'synonyms': ['bushbaby'],
     'taxid': 30611},
    {'assembly': 'KH',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('MT:7721-10971'),
     'species': 'Ciona intestinalis',
     'synonyms': ['c.intestinalis'],
     'taxid': 7719},
    {'assembly': 'CSAV 2.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('reftig_1:1336385-1336487'),
     'species': 'Ciona savignyi',
     'synonyms': ['c.savignyi'],
     'taxid': 51511},
    {'assembly': 'AstMex102',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('KB882205.1: 407,081-422,352'),
     'species': 'Astyanax mexicanus',
     'synonyms': ['cave fish'],
     'taxid': 7994},
    {'assembly': 'PelSin_1.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('MT: 1,119-2,724'),
     'species': 'Pelodiscus sinensis',
     'synonyms': ['chinese softshell turtle'],
     'taxid': 13735},
    {'assembly': 'gadMor1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('GeneScaffold_2100:13,997-14,263'),
     'species': 'Gadus morhua',
     'synonyms': ['cod'],
     'taxid': 8049},
    {'assembly': 'LatCha1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('JH130261.1: 4,943-5,243'),
     'species': 'Latimeria chalumnae',
     'synonyms': ['coelacanth'],
     'taxid': 7897},
    {'assembly': 'turTru1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('scaffold_93543:74,913-75,096'),
     'species': 'Tursiops truncatus',
     'synonyms': ['dolphin'],
     'taxid': 9739},
    {'assembly': 'BGI_duck_1.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('KB743241.1: 565,730-565,868'),
     'species': 'Anas platyrhynchos',
     'synonyms': ['duck'],
     'taxid': 8839},
    {'assembly': 'Loxafr3.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('scaffold_8:85544526-85544677'),
     'species': 'Loxodonta africana',
     'synonyms': ['elephant'],
     'taxid': 9785},
    {'assembly': 'MusPutFur1.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('GL896967.1:3146214-3253395'),
     'species': 'Mustela putorius furo',
     'synonyms': ['ferret'],
     'taxid': 9669},
    {'assembly': 'FicAlb_1.4',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('JH603221.1:2668249-2668494'),
     'species': 'Ficedula albicollis',
     'synonyms': ['flycatcher'],
     'taxid': 59894},
    {'assembly': 'FUGU 4.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('scaffold_143:290596-290698'),
     'species': 'Takifugu rubripes',
     'synonyms': ['fugu'],
     'taxid': 31033},
    {'assembly': 'Nleu1.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('GL397275.1:24223334-24223466'),
     'species': 'Nomascus leucogenys',
     'synonyms': ['gibbon'],
     'taxid': 61853},
    {'assembly': 'gorGor3.1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('14:1255367-1255699'),
     'species': 'Gorilla gorilla gorilla',
     'synonyms': ['gorilla'],
     'taxid': 9595},
    {'assembly': 'cavPor3',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': location_from_ensembl('scaffold_2:33275524-33275917'),
     'species': 'Cavia porcellus',
     'synonyms': ['guinea pig'],
     'taxid': 10141},
    {'assembly': 'eriEur1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Erinaceus europaeus',
     'synonyms': ['hedgehog'],
     'taxid': 9365},
    {'assembly': 'Equ Cab 2',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Equus caballus',
     'synonyms': ['horse'],
     'taxid': 9796},
    {'assembly': 'proCap1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Procavia capensis',
     'synonyms': ['hyrax'],
     'taxid': 9813},
    {'assembly': 'dipOrd1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Dipodomys ordii',
     'synonyms': ['kangaroo rat'],
     'taxid': 10020},
    {'assembly': 'Pmarinus_7.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Petromyzon marinus',
     'synonyms': ['lamprey'],
     'taxid': 7757},
    {'assembly': 'TENREC',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Echinops telfairi',
     'synonyms': ['lesser hedgehog tenrec'],
     'taxid': 9371},
    {'assembly': 'C_jacchus3.2.1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Callithrix jacchus',
     'synonyms': ['marmoset'],
     'taxid': 9483},
    {'assembly': 'HdrR',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Oryzias latipes',
     'synonyms': ['medaka'],
     'taxid': 8090},
    {'assembly': 'pteVam1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Pteropus vampyrus',
     'synonyms': ['megabat'],
     'taxid': 132908},
    {'assembly': 'Myoluc2.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Myotis lucifugus',
     'synonyms': ['microbat'],
     'taxid': 59463},
    {'assembly': 'Mmur_2.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Microcebus murinus',
     'synonyms': ['mouse lemur'],
     'taxid': 30608},
    {'assembly': 'PapAnu2.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Papio anubis',
     'synonyms': ['olive baboon'],
     'taxid': 9555},
    {'assembly': 'monDom5',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Monodelphis domestica',
     'synonyms': ['opossum'],
     'taxid': 13616},
    {'assembly': 'PPYG2',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Pongo abelii',
     'synonyms': ['orangutan'],
     'taxid': 9601},
    {'assembly': 'ailMel1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Ailuropoda melanoleuca',
     'synonyms': ['panda'],
     'taxid': 9646},
    {'assembly': 'Sscrofa10.2',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Sus scrofa',
     'synonyms': ['pig'],
     'taxid': 9823},
    {'assembly': 'OchPri2.0-Ens',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Ochotona princeps',
     'synonyms': ['pika'],
     'taxid': 9978},
    {'assembly': 'Xipmac4.4.2',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Xiphophorus maculatus',
     'synonyms': ['platyfish'],
     'taxid': 8083},
    {'assembly': 'OANA5',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Ornithorhynchus anatinus',
     'synonyms': ['platypus'],
     'taxid': 9258},
    {'assembly': 'OryCun2.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Oryctolagus cuniculus',
     'synonyms': ['rabbit'],
     'taxid': 9986},
    {'assembly': 'R64-1-1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Saccharomyces cerevisiae',
     'synonyms': ['s. cerevisiae'],
     'taxid': 4932},
    {'assembly': 'Oar_v3.1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Ovis aries',
     'synonyms': ['sheep'],
     'taxid': 9940},
    {'assembly': 'sorAra1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Sorex araneus',
     'synonyms': ['shrew'],
     'taxid': 42254},
    {'assembly': 'choHof1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Choloepus hoffmanni',
     'synonyms': ['sloth'],
     'taxid': 9358},
    {'assembly': 'LepOcu1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Lepisosteus oculatus',
     'synonyms': ['spotted gar'],
     'taxid': 7918},
    {'assembly': 'spetri2',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Ictidomys tridecemlineatus',
     'synonyms': ['squirrel'],
     'taxid': 43179},
    {'assembly': 'BROAD S1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Gasterosteus aculeatus',
     'synonyms': ['stickleback'],
     'taxid': 69293},
    {'assembly': 'tarSyr1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Tarsius syrichta',
     'synonyms': ['tarsier'],
     'taxid': 1868482},
    {'assembly': 'Devil_ref v7.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Sarcophilus harrisii',
     'synonyms': ['tasmanian devil'],
     'taxid': 9305},
    {'assembly': 'TETRAODON 8.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Tetraodon nigroviridis',
     'synonyms': ['tetraodon'],
     'taxid': 99883},
    {'assembly': 'Orenil1.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Oreochromis niloticus',
     'synonyms': ['tilapia'],
     'taxid': 8128},
    {'assembly': 'tupBel1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Tupaia belangeri',
     'synonyms': ['tree shrew'],
     'taxid': 37347},
    {'assembly': 'Turkey_2.01',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Meleagris gallopavo',
     'synonyms': ['turkey'],
     'taxid': 9103},
    {'assembly': 'ChlSab1.1',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Chlorocebus sabaeus',
     'synonyms': ['vervet-agm'],
     'taxid': 60711},
    {'assembly': 'Meug_1.0',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Macropus eugenii',
     'synonyms': ['wallaby'],
     'taxid': 9315},
    {'assembly': 'taeGut3.2.4',
     'assembly_ucsc': None,
     'division': 'Ensembl',
     'example_location': {'chromosome': None, 'end': None, 'start': None},
     'species': 'Taeniopygia guttata',
     'synonyms': ['zebra finch'],
     'taxid': 59729},

    # Ensembl Fungi
    # {
    #     'species': 'Saccharomyces cerevisiae',
    #     'synonyms': ['budding yeast', 'Saccharomyces cerevisiae S288c'],
    #     'assembly': 'R64-1-1',
    #     'assembly_ucsc': '',
    #     'taxid': 559292,
    #     'division': 'Ensembl Fungi',
    #     'example_location': {
    #         'chromosome': 'XII',
    #         'start': 856709,
    #         'end': 856919,
    #     },
    # },
    {
        'species': 'Schizosaccharomyces pombe',
        'synonyms': ['fission yeast'],
        'assembly': 'ASM294v2',
        'assembly_ucsc': '',
        'taxid': 4896,
        'division': 'Ensembl Fungi',
        'example_location': {
            'chromosome': 'I',
            'start': 540951,
            'end': 544327,
        },
    },
    # Ensembl Metazoa
    {
        'species': 'Caenorhabditis elegans',
        'synonyms': ['worm'],
        'assembly': 'WBcel235',
        'assembly_ucsc': '',
        'taxid': 6239,
        'division': 'Ensembl Metazoa',
        'example_location': {
            'chromosome': 'III',
            'start': 11467363,
            'end': 11467705,
        },
    },
    {
        'species': 'Drosophila melanogaster',
        'synonyms': ['fly'],
        'assembly': 'BDGP6',
        'assembly_ucsc': 'dm6',
        'taxid': 7227,
        'division': 'Ensembl Metazoa',
        'example_location': {
            'chromosome': '3R',
            'start': 7474331,
            'end': 7475217,
        },
    },
    {
        'species': 'Bombyx mori',
        'synonyms': ['silkworm'],
        'assembly': 'GCA_000151625.1',
        'assembly_ucsc': '',
        'taxid': 7091,
        'division': 'Ensembl Metazoa',
        'example_location': {
            'chromosome': 'scaf16',
            'start': 6180018,
            'end': 6180422,
        },
    },
    # {
    #     'species': 'Anopheles gambiae',
    #     'synonyms': [],
    #     'assembly': 'AgamP4',
    #     'assembly_ucsc': '',
    #     'taxid': 7165,
    #     'division': 'Ensembl Metazoa',
    #     'example_location': {
    #         'chromosome': '2R',
    #         'start': 34644956,
    #         'end': 34645131,
    #     },
    # },
    # Ensembl Protists
    # {
    #     'species': 'Dictyostelium discoideum',
    #     'synonyms': [],
    #     'assembly': 'dictybase.01',
    #     'assembly_ucsc': '',
    #     'taxid': 44689,
    #     'division': 'Ensembl Protists',
    #     'example_location': {
    #         'chromosome': 2,
    #         'start': 7874546,
    #         'end': 7876498,
    #     },
    # },
    # {
    #     'species': 'Plasmodium falciparum',
    #     'synonyms': [],
    #     'assembly': 'ASM276v1',
    #     'assembly_ucsc': '',
    #     'taxid': 5833,
    #     'division': 'Ensembl Protists',
    #     'example_location': {
    #         'chromosome': 13,
    #         'start': 2796339,
    #         'end': 2798488,
    #     },
    # },
    # Ensembl Plants
    {
        'species': 'Arabidopsis thaliana',
        'synonyms': [],
        'assembly': 'TAIR10',
        'assembly_ucsc': '',
        'taxid': 3702,
        'division': 'Ensembl Plants',
        'example_location': {
            'chromosome': 2,
            'start': 18819643,
            'end': 18822629,
        },
    },
]
