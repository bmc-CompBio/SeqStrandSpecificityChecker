#!/usr/bin/env python

from SeqStrandSpecificityChecker import SeqStrandSpecificityChecker

import subprocess
import sys

arguments = sys.argv

if len(arguments) != 3:
    print("Usage: python main.py <bowtie2_directory> <gene_seq> <reference_genome>")
    sys.exit(1)

bowtie2_directory, gene_seq, reference_genome = sys.argv[1], sys.argv[2], sys.argv[3]
SeqStrandSpecificityChecker(bowtie2_directory, gene_seq, reference_genome)

""""
directory = "/Users/timkiebler/Documents/Uni/informatik/Bachelorarbeit/test_data"
reference_genome = directory + "/mouse_references.fa"
gene_seq = directory + "/SRR16474730_2.fastq"
bowtie2_directory = "/Users/timkiebler/anaconda3/pkgs/bowtie2-2.2.5-0"

seq_strand_specificity_checker = SeqStrandSpecificityChecker(bowtie2_directory, gene_seq, reference_genome)

test command for my mac: 
  ./main.py /Users/timkiebler/anaconda3/pkgs/bowtie2-2.2.5-0
            /Users/timkiebler/Documents/Uni/informatik/Bachelorarbeit/test_data/SRR16474730_2.fastq 
            /Users/timkiebler/Documents/Uni/informatik/Bachelorarbeit/test_data/mouse_references.fa
"""