from .utils import is_first_file, is_header, split_columns, contains_field


def annotate_filter_values(file_idx, line):
    if not line.startswith('#'):
        line = split_columns(line)
        if not contains_field(line[8], 'FT'):
            line[8] += ':FT'
            line[-1] = line[-1].rstrip() + ':' + line[6] + '\n'
            line[6] = '.'
        line = '\t'.join(line)
    return line


def strip_fixed_columns(file_idx, line):
    if not is_first_file(file_idx) and not is_header(line):
        line = split_columns(line)[-1]

    return line
