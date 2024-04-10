import subprocess
import os


def check_file(path):
    """
    Check the existence and accessibility of a file at the specified path.

    :param path: A string representing the file path to be checked.
    :type path: str

    :raises FileNotFoundError: If the file does not exist.
    :raises PermissionError: If there are permission issues when trying to open the file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError("The file " + path + " does not exist. \n")

    if not os.path.isfile(path):
        raise FileNotFoundError("The path " + path + " exists, but it is not a file. \n")

    try:
        with open(path, 'r') as file:
            pass
    except PermissionError as e:
        raise PermissionError("Permission error while opening " + path + "\n")


def create_directory(directory_name):
    """
    Create a directory with the specified name and return its absolute path.

    :param directory_name: A string representing the name of the directory to be created.
    :type directory_name: str

    :return: The absolute path of the created directory.
    :rtype: str
    """
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    return os.path.abspath(directory_name)


def get_extension(file_name):
    """
    Extracts and returns the file extension from a filename.

    :param file_name: The input string from which to extract the extension.
    :type file_name: str

    :return: The file extension, excluding the period ('.').
    :rtype: str

    :raises ValueError: If the input string does not contain a period ('.').
    """
    last_dot_index = file_name.rfind(".")

    if last_dot_index != -1:
        extension = file_name[last_dot_index + 1:]
        return extension
    else:
        raise ValueError("The input file is not in a correct format.")


def create_sample_with_given_size(input_file_path, sample_size):
    """
    Create a sample file by extracting the first x lines from the input file.

    :param input_file_path: The path to the input file to extract data from.
    :type: str

    :param sample_size: The number of lines that should be extracted from the input file.
    :type: int

    :return: The name of the created sample file.
    :rtype: str
    """
    with open(input_file_path, 'r') as input_file:
        extension = get_extension(input_file_path)
        output_file_name = "sample" + extension
        with open(output_file_name, 'w') as output_file:
            for i, line in enumerate(input_file):
                if i >= sample_size:
                    break
                output_file.write(line)
        return output_file_name


def create_sample_with_given_size2(input_file_path, starting_from_line, sample_size):
    """
    Create a sample file by extracting the first x lines from the input file.

    :param input_file_path: The path to the input file to extract data from.
    :type: str

    :param starting_from_line:
    :type: int

    :param sample_size: The number of lines that should be extracted from the input file.
    :type: int

    :return: The name of the created sample file.
    :rtype: str
    """
    with open(input_file_path, 'r') as input_file:
        extension = get_extension(input_file_path)
        output_file_name = "sample" + extension
        with open(output_file_name, 'w') as output_file:
            for i, line in enumerate(input_file):
                if i >= sample_size + starting_from_line:
                    break
                if i >= starting_from_line:
                    output_file.write(line)
        return output_file_name


class SeqStrandSpecificityChecker:

    def __init__(self, gene_seq, reference_genome):
        self.gene_seq = gene_seq
        self.reference_genome = reference_genome
        self.name_index_dir = "index"

        check_file(self.reference_genome)
        check_file(self.gene_seq)

        self.index_reference_genome()

        sample_size = 100000
        sample = create_sample_with_given_size(gene_seq, sample_size)

        mapped_reads = self.run_bowtie2_alignment(sample)

        os.remove(sample)

        num_negative_reads, num_positive_reads = self.count_positve_and_negative_reads(mapped_reads)

        os.remove(mapped_reads)

        portion_pos_reads, portion_neg_reads = self.calculate_ratio(num_positive_reads, num_negative_reads)

        end_result = self.evaluate_result(portion_pos_reads, portion_neg_reads)

        self.print_end_result(end_result, num_negative_reads, num_positive_reads)

    def get_bowtie2_dir(self):
        """
            Retrieve the directory path of Bowtie 2 specified by the BT2_HOME environment variable.

            :return: the path to the directory in which the bowtie2 executable is stored.
        """
        bowtie2_dir = subprocess.check_output('echo $BT2_HOME', shell=True, text=True).strip()
        return bowtie2_dir

    def index_reference_genome(self):
        """
        This function creates an index for a reference genome using Bowtie 2. The indexed files are
        generated in a newly made directory.

        :raises subprocess.CalledProcessError: If an error occurs during the execution of the 'bowtie2-build' command.
        :return: None
        """
        index_dir = create_directory(self.name_index_dir)
        os.chdir(index_dir)

        # Run the bowtie2-build command
        subprocess.run(["bowtie2-build", self.reference_genome, "mouse"], stdout=subprocess.DEVNULL)

        os.chdir("..")


    def run_bowtie2_alignment(self, gene_seq):
        """
        This function performs an alignment using Bowtie 2 with a reference genome index that has to
        be previously created. The alignment results are saved in a SAM format file named "result.sam"
        in the current working directory.

        :param gene_seq: The path to the gene sequence file to be aligned.
        :type gene_seq: str

        :raises subprocess.CalledProcessError: If an error occurs during the execution of the Bowtie 2 alignment command.

        :return: The name of the SAM format result file generated by the alignment.
        :rtype: str
        """
        name_result_file = "result.sam"
        with open(name_result_file, "w") as file:
            pass

        bowtie2_command = ("bowtie2 -x " + self.name_index_dir + "/mouse" +
                           " -U " + gene_seq + " -S " + name_result_file)

        try:
            subprocess.run(bowtie2_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        return name_result_file

    def count_positve_and_negative_reads(self, result_file):
        """
        This function reads a SAM format result file and counts the number of positive and negative
        reads based on the second field of each SAM alignment. The interpretation of this field is
        determined according to the Bowtie 2 manual, which provides the specification for SAM flags.
        You can find the detailed flag descriptions in the Bowtie 2 manual:
        https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#sam-output

        :param result_file: The path to the SAM format result file to be analyzed.
        :type result_file: str

        :return: A tuple containing the count of negative reads and the count of positive reads.
        :rtype: tuple (int, int)
        """
        # Open the input file for reading
        with open(result_file, "r") as input_file:
            # An empty set to keep track of seen read names
            seen_read_names = set()
            paired_reads = []

            num_positive_reads = 0
            num_negative_reads = 0

            for line in input_file:
                fields = line.split('\t')
                flag = fields[1]
                if flag == "0":  # The flag bit 0x1 indicates it's a paired-end read
                    num_positive_reads = num_positive_reads + 1
                    paired_reads.append(line)
                elif flag == "16" or flag == str(16 + 64) or flag == str(16 + 1):
                    num_negative_reads = num_negative_reads + 1
                    paired_reads.append(line)
        return num_negative_reads, num_positive_reads

    def evaluate_result(self, portion_pos_reads, portion_neg_reads):
        """
        Evaluate the result of read alignments to determine the strand specificity.

        This function takes the ratio of negative and positive reads and evaluates the result to determine the strand
        specificity of the read alignments. It returns one of the following values:

        - "Negative" if there are more than 90 percent negative reads, indicating a preference for the negative strand.
        - "Positive" if there are more than 90 percent positive reads, indicating a preference for the positive strand.
        - "Unstranded" otherwise

        :param portion_pos_reads: The ratio of positive reads to the total reads (rounded to 3 decimal places).
        :type portion_pos_reads: float
        :param portion_neg_reads: The ratio of negative reads to the total reads (rounded to 3 decimal places).
        :type portion_neg_reads: float

        :return: A string indicating the strand specificity of the read alignments.
        :rtype: str
        """
        if portion_pos_reads < 0.9 and portion_neg_reads < 0.9:
            return "Unstranded"
        elif portion_neg_reads >= 0.9 and portion_pos_reads <= 0.1:
            return "negative"
        elif portion_neg_reads >= 0 and portion_pos_reads <= 0:
            return "positive"

    def calculate_ratio(self, num_positive_reads, num_negative_reads):
        """
        Calculate the ratio of positive and negative reads in a dataset.

        :param num_positive_reads: The number of positive reads in the dataset.
        :type: int
        :param num_negative_reads: The number of negative reads in the dataset.
        :type: int

        :return: portion_pos_reads: The ratio of positive reads to the total reads (rounded to 3 decimal places).
        :rtype float
        :return: portion_neg_reads: The ratio of negative reads to the total reads (rounded to 3 decimal places).
        :rtype float
        """
        num_reads = num_positive_reads + num_negative_reads
        portion_pos_reads = round(num_positive_reads / num_reads, 3)
        portion_neg_reads = round(num_negative_reads / num_reads, 3)
        return portion_pos_reads, portion_neg_reads

    def print_end_result(self, end_result, num_negative_reads, num_positive_reads):
        print("\n_________________________")
        print("\nResult: " + str(end_result))

        if end_result == "Unstranded":
            portion_pos_reads, portion_neg_reads = self.calculate_ratio(num_negative_reads, num_positive_reads)
            print("Ratio: " + str(portion_pos_reads) + " positive, " + str(portion_neg_reads) + " negative ")

        print("\n\n")

