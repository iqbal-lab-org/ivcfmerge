import itertools

from utils import assign_file_index_to_lines, parse_data, is_first_file, is_header, write_vcf


def merge_vcf_files(input_paths, output_path):

    # An iterator through the files (which are iterators through their lines)
    # [
    #  [line, line, ...],  # file 1
    #  [line, line, ...],  # file 2
    #  ...
    # ]
    files = map(lambda p: open(p, 'r'), input_paths)

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

    # Parse and transform each line accordingly
    # Add additional transformers here
    # [
    #  (0, header),
    #  (1, header),
    #  ...
    #  (0, fixed + genotype),
    #  (1, genotype),
    #  ...
    # ]
    parsed = itertools.starmap(parse_data, flatten)

    # Filter unwanted lines (duplicated headers, FILTER!=PASS, etc.)
    # Add additional filters here
    # [
    #  (0, header),
    #  ...
    #  (0, fixed + genotype),
    #  (1, genotype),
    #  ...
    # ]
    deduped = filter(lambda item: is_first_file(item[0]) or not is_header(item[1]), parsed)

    # Actually iterate the lines and write them
    write_vcf(deduped, output_path, len(input_paths))
