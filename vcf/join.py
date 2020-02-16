import argparse

from vcf.reader import MultiVCFReader

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Join genotype data from multiple VCF files.")
    parser.add_argument('input_paths', type=str, help="a file where each line is the path to one of the VCF"
                                                      "files that need be be joined")
    parser.add_argument('output_path', type=str, help="where to write the joined VCF")
    args = parser.parse_args()

    input_paths = open(args.input_paths, 'r').read().splitlines()

    with open(args.output_path, 'w') as out_file:
        with MultiVCFReader(input_paths) as reader:
            for line in reader:
                out_file.write(line)
