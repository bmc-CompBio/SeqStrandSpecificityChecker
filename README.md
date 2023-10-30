# SeqStrandSpecificityChecker

To ensure the program functions correctly, Bowtie2 must be installed, and the BT2_HOME environment variable
must be configured as specified in the Bowtie2 manual, pointing to the new Bowtie 2 directory containing the
bowtie2, bowtie2-build and bowtie2-inspect binaries.

To run the program, simply execute the following command in your terminal:
"/<SeqStrandSpecificityChecker_dir> checkStrandSpecificity <gene_seq> <reference_genome>"

In the command above, replace <SeqStrandSpecificityChecker_directory>, <gene_seq> and <reference_genome> with
the actual paths to the SeqStrandSpecificityChecker tool, the file containing the gene sequence you want to
analyze, and the directory of your reference genome, as required for your analysis.

The results should be printed out on your console.

Example result:

[...]
_________________________

Result: Unstranded
Ratio: 0.045 positive, 0.955 negantive
