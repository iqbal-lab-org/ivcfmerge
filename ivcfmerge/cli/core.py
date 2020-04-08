import argparse
from contextlib import ExitStack

from ivcfmerge import ivcfmerge


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_paths_file', type=str)
    parser.add_argument('output_path', type=str)
    args = parser.parse_args()

    with open(args.input_paths_file, 'r') as input_paths_file:
        input_paths = input_paths_file.read().splitlines()

        with ExitStack() as stack, open(args.output_path, 'w') as outfile:
            infiles = map(lambda p: stack.enter_context(open(p)), input_paths)
            ivcfmerge(infiles, outfile)
