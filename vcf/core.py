import itertools
from contextlib import ExitStack

from .filters import not_subsequent_header
from .transformers import strip_fixed_columns
from .utils import assign_file_index_to_lines, write_vcf


def merge_vcf_files(input_paths, output_path):
    with ExitStack() as stack:
        # An iterator through the files (which are iterators through their lines)
        # [
        #  [line, line, ...],  # file 1
        #  [line, line, ...],  # file 2
        #  ...
        # ]
        files = map(lambda p: stack.enter_context(open(p, 'r')), input_paths)

        # An iterator through the files with their indices
        # [
        #  (0, [line, line, ...]),  # file 1
        #  (1, [line, line, ...]),  # file 2
        #  ...
        # ]
        file_enumerator = enumerate(files)

        # Insert to each line of each file their file's index
        # [
        #  [
        #   (0, line),
        #   (0, line),
        #   ...
        #  ],  # file 1
        #  [
        #   (1, line),
        #   (1, line),
        #   ...
        #  ],  # file 2
        #  ...
        # ]
        file_indexed_lines = itertools.starmap(assign_file_index_to_lines, file_enumerator)

        # Group lines of the same row together
        # [
        #  [
        #   (0, line),
        #   (1, line),
        #   ...
        #  ],  # all first lines
        #  [
        #   (0, line),
        #   (1, line),
        #   ...
        #  ],  # all second lines
        #  ...
        # ]
        grouped_by_row = zip(*file_indexed_lines)

        # Flatten them, so that iterating them will only yield one line of one file (hence low memory)
        # [
        #  (0, line),
        #  (1, line),
        #  ...
        #  (0, line),
        #  (1, line),
        #  ...
        # ]
        flatten = itertools.chain.from_iterable(grouped_by_row)

        # Transform each line accordingly
        # [
        #  (0, header),
        #  (1, header),
        #  ...
        #  (0, fixed + genotype),
        #  (1, genotype),
        #  ...
        # ]
        transformed = itertools.starmap(transform, flatten)

        # Filter unwanted lines (duplicated headers, FILTER!=PASS, etc.)
        # [
        #  (0, header),
        #  ...
        #  (0, fixed + genotype),
        #  (1, genotype),
        #  ...
        # ]
        filtered = apply_filters(transformed)

        # Actually iterate the lines and write them
        with open(output_path, 'w') as out_file:
            write_vcf(filtered, out_file, len(input_paths))


def transform(file_idx, line):
    line = strip_fixed_columns(file_idx, line)

    # Add additional transformers here, each should be a function that receives a (file index, line) argument pair and
    # returns the transformed line

    return file_idx, line


def apply_filters(items):
    items = filter(not_subsequent_header, items)

    # Add additional filters here, each should be a function that receives a (file index, line) tuple and returns a bool

    return items