def assign_file_index_to_lines(file_idx, lines):
    return map(lambda line: (file_idx, line), lines)


def is_first_file(file_idx):
    return file_idx == 0


def is_header(line):
    return line.startswith('##')


def split_columns(line):
    return line.split('\t', maxsplit=9)


def join_columns(columns):
    return '\t'.join(columns)


def contains_field(column, field):
    return ':%s' % field in column or '%s:' % field in column


def add_field(column, field):
    return column + ':' + field


def write_vcf(lines, outfile, n_input_files):
    """Iterate and write header and data lines correctly

    Keyword arguments:
    lines - a list of (file index, content) tuples
    out_file - file handle of the file to write to
    n_input_files - precomputed total number of input files, so that this function can put newlines correctly in the
                    final output
    """
    for file_idx, line in lines:
        if file_idx < n_input_files - 1 and not is_header(line):
            line = line.rstrip() + '\t'

        outfile.write(line)
