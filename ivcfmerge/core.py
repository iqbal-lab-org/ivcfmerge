import itertools

from .filters import not_subsequent_header
from .transformers import strip_fixed_columns
from .utils import assign_file_index_to_lines, write_vcf


def ivcfmerge(infiles, outfile):
    infiles_1, infiles_2 = itertools.tee(infiles)
    n_infiles = len(list(infiles_1))

    # Create an iterator through the files with their indices
    # [
    #  (0, [line, line, ...]),  # file 1
    #  (1, [line, line, ...]),  # file 2
    #  ...
    # ]
    file_enumerator = enumerate(infiles_2)

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
    write_vcf(filtered, outfile, n_infiles)


def transform(file_idx, line):
    line = strip_fixed_columns(file_idx, line)

    # Add additional transformers here, each should be a function that receives a (file index, line) argument pair and
    # returns the transformed line

    return file_idx, line


def apply_filters(items):
    items = filter(not_subsequent_header, items)

    # Add additional filters here, each should be a function that receives a (file index, line) tuple and returns a bool

    return items
