# SeqStrandSpecificityChecker

To ensure the program functions correctly, Bowtie2 must be installed.

To run the program, simply execute the following command in your terminal:
"/<SeqStrandSpecificityChecker_dir> checkStrandSpecificity <gene_seq> <reference_genome>"

In the command above, replace <SeqStrandSpecificityChecker_directory>, <gene_seq> and <reference_genome> with
the actual paths to the SeqStrandSpecificityChecker tool, the file containing the gene sequence you want to
analyze, and the directory of your reference genome, as required for your analysis.

The results should be printed out on your console.

Example result:

[...]
100000 reads; of these:
  100000 (100.00%) were unpaired; of these:
    99887 (99.89%) aligned 0 times
    113 (0.11%) aligned exactly 1 time
    0 (0.00%) aligned >1 times
0.11% overall alignment rate
_________________________

Result: Unstranded
Ratio: 0.045 positive, 0.955 negantive
