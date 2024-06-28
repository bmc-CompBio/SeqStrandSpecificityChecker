#!/usr/bin/env python3

from SeqStrandSpecificityChecker import SeqStrandSpecificityChecker

import sys

arguments = sys.argv

if len(arguments) < 4 or len(arguments) > 5 or arguments[1] != "checkStrandSpecificity":
    print("Usage: /<SeqStrandSpecificityChecker_dir> checkStrandSpecificity <gene_seq>"
          " <reference_genome> [sample size]")
    sys.exit(1)

gene_seq, reference_genome = arguments[2], arguments[3]


def handle_optional_arg(arg):
    try:
        return int(arg)
    except ValueError:
        print(f"Error: {arg} is not a valid integer.")
        sys.exit(1)


if len(arguments) == 5:
    sample_size = handle_optional_arg(arguments[4])
    SeqStrandSpecificityChecker(gene_seq, reference_genome, sample_size)
else:
    SeqStrandSpecificityChecker(gene_seq, reference_genome)