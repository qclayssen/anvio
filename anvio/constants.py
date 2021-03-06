# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

import os
import sys
import glob
import string

from collections import Counter

import anvio

__author__ = "Developers of anvi'o (see AUTHORS.txt)"
__copyright__ = "Copyleft 2015-2018, the Meren Lab (http://merenlab.org/)"
__credits__ = []
__license__ = "GPL 3.0"
__maintainer__ = "A. Murat Eren"
__email__ = "a.murat.eren@gmail.com"
__status__ = "Development"


clustering_configs_dir = os.path.join(os.path.dirname(anvio.__file__), 'data/clusterconfigs')
clustering_configs = {}

default_port_number = int(os.environ['ANVIO_PORT']) if 'ANVIO_PORT' in os.environ else 8080

blank_default = "tnf"
single_default = "tnf"
merged_default = "tnf-cov"
pan_default = "presence-absence"

default_gene_caller = "prodigal"

max_num_items_for_hierarchical_clustering = 20000

# default methods for hierarchical cluster analyses
distance_metric_default = 'euclidean'
linkage_method_default = 'ward'

# this is to have a common language across multiple modules when genomes (whether they are MAGs,
# SAGs, or isolate genomes):
essential_genome_info = ['gc_content', 'num_contigs', 'num_splits', 'total_length', 'num_genes', 'percent_completion', 'percent_redundancy',
                         'genes_are_called', 'avg_gene_length', 'num_genes_per_kb', ]

levels_of_taxonomy = ["t_domain", "t_phylum", "t_class", "t_order", "t_family", "t_genus", "t_species"]

for run_type_and_default_config_tuples in [('single', single_default), ('merged', merged_default), ('blank', blank_default)]:
    run_type, default_config = run_type_and_default_config_tuples
    if not os.path.exists(os.path.join(clustering_configs_dir, run_type, default_config)):
        print("Error: The default clustering configuration file for %s runs, '%s',\n\
       is missing from data/clusterconfigs dir! I don't know how this happened,\n\
       but I can't fix this! Anvi'o needs an adult :(" % (run_type, default_config))
        sys.exit()

for dir in [d.strip('/').split('/')[-1] for d in glob.glob(os.path.join(clustering_configs_dir, '*/'))]:
    clustering_configs[dir] = {}
    for config in glob.glob(os.path.join(clustering_configs_dir, dir, '*')):
        clustering_configs[dir][os.path.basename(config)] = config

IS_ESSENTIAL_FIELD = lambda f: (not f.startswith('__')) and (f not in ["contig", "GC_content", "length"])
IS_AUXILIARY_FIELD = lambda f: f.startswith('__')
allowed_chars = string.ascii_letters + string.digits + '_' + '-' + '.'
digits = string.digits
complements = str.maketrans('acgtrymkbdhvACGTRYMKBDHV', 'tgcayrkmvhdbTGCAYRKMVHDB')

nucleotides = sorted(list('ATCG')) + ['N']

AA_atomic_composition = Counter({'Ala': {"C":3,  "H":7,  "N":1, "O":2, "S":0},
                                 'Arg': {"C":6,  "H":14, "N":4, "O":2, "S":0},
                                 'Asn': {"C":4,  "H":8,  "N":2, "O":3, "S":0},
                                 'Asp': {"C":4,  "H":7,  "N":1, "O":4, "S":0},
                                 'Cys': {"C":3,  "H":7,  "N":1, "O":2, "S":1},
                                 'Gln': {"C":5,  "H":10, "N":2, "O":3, "S":0},
                                 'Glu': {"C":5,  "H":9,  "N":1, "O":4, "S":0},
                                 'Gly': {"C":2,  "H":5,  "N":1, "O":2, "S":0},
                                 'His': {"C":6,  "H":9,  "N":3, "O":2, "S":0},
                                 'Ile': {"C":6,  "H":13, "N":1, "O":2, "S":0},
                                 'Leu': {"C":6,  "H":13, "N":1, "O":2, "S":0},
                                 'Lys': {"C":6,  "H":14, "N":2, "O":2, "S":0},
                                 'Met': {"C":5,  "H":11, "N":1, "O":2, "S":1},
                                 'Phe': {"C":9,  "H":11, "N":1, "O":2, "S":0},
                                 'Pro': {"C":5,  "H":9,  "N":1, "O":2, "S":0},
                                 'Ser': {"C":3,  "H":7,  "N":1, "O":3, "S":0},
                                 'Thr': {"C":4,  "H":9,  "N":1, "O":3, "S":0},
                                 'Trp': {"C":11, "H":12, "N":2, "O":2, "S":0},
                                 'Tyr': {"C":9,  "H":11, "N":1, "O":3, "S":0},
                                 'Val': {"C":5,  "H":11, "N":1, "O":2, "S":0}})

AA_to_codons = Counter({'Ala': ['GCA', 'GCC', 'GCG', 'GCT'],
                        'Arg': ['AGA', 'AGG', 'CGA', 'CGC', 'CGG', 'CGT'],
                        'Asn': ['AAC', 'AAT'],
                        'Asp': ['GAC', 'GAT'],
                        'Cys': ['TGC', 'TGT'],
                        'Gln': ['CAA', 'CAG'],
                        'Glu': ['GAA', 'GAG'],
                        'Gly': ['GGA', 'GGC', 'GGG', 'GGT'],
                        'His': ['CAC', 'CAT'],
                        'Ile': ['ATA', 'ATC', 'ATT'],
                        'Leu': ['CTA', 'CTC', 'CTG', 'CTT', 'TTA', 'TTG'],
                        'Lys': ['AAA', 'AAG'],
                        'Met': ['ATG'],
                        'Phe': ['TTC', 'TTT'],
                        'Pro': ['CCA', 'CCC', 'CCG', 'CCT'],
                        'STP': ['TAA', 'TAG', 'TGA'],
                        'Ser': ['AGC', 'AGT', 'TCA', 'TCC', 'TCG', 'TCT'],
                        'Thr': ['ACA', 'ACC', 'ACG', 'ACT'],
                        'Trp': ['TGG'],
                        'Tyr': ['TAC', 'TAT'],
                        'Val': ['GTA', 'GTC', 'GTG', 'GTT']})

AA_to_single_letter_code = Counter({'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D',
                                    'Cys': 'C', 'Gln': 'Q', 'Glu': 'E', 'Gly': 'G',
                                    'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K',
                                    'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'STP': '*',
                                    'Ser': 'S', 'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y',
                                    'Val': 'V'})

amino_acids = sorted(list(AA_to_single_letter_code.keys()))

codon_to_AA = Counter({'ATA': 'Ile', 'ATC': 'Ile', 'ATT': 'Ile', 'ATG': 'Met',
                       'ACA': 'Thr', 'ACC': 'Thr', 'ACG': 'Thr', 'ACT': 'Thr',
                       'AAC': 'Asn', 'AAT': 'Asn', 'AAA': 'Lys', 'AAG': 'Lys',
                       'AGC': 'Ser', 'AGT': 'Ser', 'AGA': 'Arg', 'AGG': 'Arg',
                       'CTA': 'Leu', 'CTC': 'Leu', 'CTG': 'Leu', 'CTT': 'Leu',
                       'CCA': 'Pro', 'CCC': 'Pro', 'CCG': 'Pro', 'CCT': 'Pro',
                       'CAC': 'His', 'CAT': 'His', 'CAA': 'Gln', 'CAG': 'Gln',
                       'CGA': 'Arg', 'CGC': 'Arg', 'CGG': 'Arg', 'CGT': 'Arg',
                       'GTA': 'Val', 'GTC': 'Val', 'GTG': 'Val', 'GTT': 'Val',
                       'GCA': 'Ala', 'GCC': 'Ala', 'GCG': 'Ala', 'GCT': 'Ala',
                       'GAC': 'Asp', 'GAT': 'Asp', 'GAA': 'Glu', 'GAG': 'Glu',
                       'GGA': 'Gly', 'GGC': 'Gly', 'GGG': 'Gly', 'GGT': 'Gly',
                       'TCA': 'Ser', 'TCC': 'Ser', 'TCG': 'Ser', 'TCT': 'Ser',
                       'TTC': 'Phe', 'TTT': 'Phe', 'TTA': 'Leu', 'TTG': 'Leu',
                       'TAC': 'Tyr', 'TAT': 'Tyr', 'TAA': 'STP', 'TAG': 'STP',
                       'TGC': 'Cys', 'TGT': 'Cys', 'TGA': 'STP', 'TGG': 'Trp'})

codon_to_AA_RC = Counter({'AAA': 'Phe', 'AAC': 'Val', 'AAG': 'Leu', 'AAT': 'Ile',
                          'ACA': 'Cys', 'ACC': 'Gly', 'ACG': 'Arg', 'ACT': 'Ser',
                          'AGA': 'Ser', 'AGC': 'Ala', 'AGG': 'Pro', 'AGT': 'Thr',
                          'ATA': 'Tyr', 'ATC': 'Asp', 'ATG': 'His', 'ATT': 'Asn',
                          'CAA': 'Leu', 'CAC': 'Val', 'CAG': 'Leu', 'CAT': 'Met',
                          'CCA': 'Trp', 'CCC': 'Gly', 'CCG': 'Arg', 'CCT': 'Arg',
                          'CGA': 'Ser', 'CGC': 'Ala', 'CGG': 'Pro', 'CGT': 'Thr',
                          'CTA': 'STP', 'CTC': 'Glu', 'CTG': 'Gln', 'CTT': 'Lys',
                          'GAA': 'Phe', 'GAC': 'Val', 'GAG': 'Leu', 'GAT': 'Ile',
                          'GCA': 'Cys', 'GCC': 'Gly', 'GCG': 'Arg', 'GCT': 'Ser',
                          'GGA': 'Ser', 'GGC': 'Ala', 'GGG': 'Pro', 'GGT': 'Thr',
                          'GTA': 'Tyr', 'GTC': 'Asp', 'GTG': 'His', 'GTT': 'Asn',
                          'TAA': 'Leu', 'TAC': 'Val', 'TAG': 'Leu', 'TAT': 'Ile',
                          'TCA': 'STP', 'TCC': 'Gly', 'TCG': 'Arg', 'TCT': 'Arg',
                          'TGA': 'Ser', 'TGC': 'Ala', 'TGG': 'Pro', 'TGT': 'Thr',
                          'TTA': 'STP', 'TTC': 'Glu', 'TTG': 'Gln', 'TTT': 'Lys'})

codon_to_codon_RC = Counter({'AAA': 'TTT', 'AAC': 'GTT', 'AAG': 'CTT', 'AAT': 'ATT',
                             'ACA': 'TGT', 'ACC': 'GGT', 'ACG': 'CGT', 'ACT': 'AGT',
                             'AGA': 'TCT', 'AGC': 'GCT', 'AGG': 'CCT', 'AGT': 'ACT',
                             'ATA': 'TAT', 'ATC': 'GAT', 'ATG': 'CAT', 'ATT': 'AAT',
                             'CAA': 'TTG', 'CAC': 'GTG', 'CAG': 'CTG', 'CAT': 'ATG',
                             'CCA': 'TGG', 'CCC': 'GGG', 'CCG': 'CGG', 'CCT': 'AGG',
                             'CGA': 'TCG', 'CGC': 'GCG', 'CGG': 'CCG', 'CGT': 'ACG',
                             'CTA': 'TAG', 'CTC': 'GAG', 'CTG': 'CAG', 'CTT': 'AAG',
                             'GAA': 'TTC', 'GAC': 'GTC', 'GAG': 'CTC', 'GAT': 'ATC',
                             'GCA': 'TGC', 'GCC': 'GGC', 'GCG': 'CGC', 'GCT': 'AGC',
                             'GGA': 'TCC', 'GGC': 'GCC', 'GGG': 'CCC', 'GGT': 'ACC',
                             'GTA': 'TAC', 'GTC': 'GAC', 'GTG': 'CAC', 'GTT': 'AAC',
                             'TAA': 'TTA', 'TAC': 'GTA', 'TAG': 'CTA', 'TAT': 'ATA',
                             'TCA': 'TGA', 'TCC': 'GGA', 'TCG': 'CGA', 'TCT': 'AGA',
                             'TGA': 'TCA', 'TGC': 'GCA', 'TGG': 'CCA', 'TGT': 'ACA',
                             'TTA': 'TAA', 'TTC': 'GAA', 'TTG': 'CAA', 'TTT': 'AAA'})

codons = sorted(list(set(codon_to_AA.keys())))

pretty_names = {}

def get_pretty_name(key):
    if key in pretty_names:
        return pretty_names[key]
    else:
        return key
