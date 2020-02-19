def assign_file_index_to_lines(file_idx, lines):
    return map(lambda line: (file_idx, line), lines)


def parse_data(file_idx, line):
    if not is_first_file(file_idx) and not is_header(line):
        line = line.split('\t', maxsplit=9)[-1]

    return file_idx, line


def is_first_file(file_idx):
    return file_idx == 0


def is_header(line):
    return line.startswith('##')


def write_vcf(lines, output_path, n_input_files):
    """Iterate and write header and data lines correctly

    Keyword arguments:
    n_input_files - precomputed total number of input files, so that this function can put newlines correctly in the
                    final output
    """
    with open(output_path, 'w') as out_file:
        for file_idx, line in lines:
            if file_idx < n_input_files - 1 and not is_header(line):
                line = line.rstrip() + '\t'

            out_file.write(line)
