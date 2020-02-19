import argparse

from core import merge_vcf_files

parser = argparse.ArgumentParser()
parser.add_argument('file_of_input_paths', type=str)
parser.add_argument('output_path', type=str)
args = parser.parse_args()

input_paths = open(args.file_of_input_paths, 'r').read().splitlines()
merge_vcf_files(input_paths, args.output_path)
