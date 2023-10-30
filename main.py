#!/usr/bin/env python3

from SeqStrandSpecificityChecker import SeqStrandSpecificityChecker

import sys

arguments = sys.argv

if len(arguments) != 4 or arguments[1] != "checkStrandSpecificity":
    print("Usage: ./<SeqStrandSpecificityChecker_directory> checkStrandSpecificity <gene_seq>"
          " <reference_genome>")
    sys.exit(1)

gene_seq, reference_genome = sys.argv[2], sys.argv[3]
SeqStrandSpecificityChecker(gene_seq, reference_genome)
