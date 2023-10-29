#!/usr/bin/env python3

from SeqStrandSpecificityChecker import SeqStrandSpecificityChecker

import subprocess
import sys

arguments = sys.argv

if len(arguments) != 5 or arguments[1] != "checkStrandSpecificity":
    print("Usage: ./<SeqStrandSpecificityChecker_directory> checkStrandSpecificity <bowtie2_directory> <gene_seq>"
          " <reference_genome>")
    sys.exit(1)

bowtie2_directory, gene_seq, reference_genome = sys.argv[2], sys.argv[3], sys.argv[4]
SeqStrandSpecificityChecker(bowtie2_directory, gene_seq, reference_genome)
