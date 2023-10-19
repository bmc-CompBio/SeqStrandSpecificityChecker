from SeqStrandSpecificityChecker import SeqStrandSpecificityChecker

directory = "/Users/timkiebler/Documents/Uni/informatik/Bachelorarbeit/test_data"
reference_genome = directory + "/mouse_references.fa"
gene_seq = directory + "/SRR4435526.fastq"
bowtie2_directory = "/Users/timkiebler/anaconda3/pkgs/bowtie2-2.2.5-0"

seq_strand_specificity_checker = SeqStrandSpecificityChecker(bowtie2_directory, gene_seq, reference_genome)
