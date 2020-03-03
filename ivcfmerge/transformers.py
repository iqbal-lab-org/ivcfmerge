from .utils import is_first_file, is_header


def annotate_filter_values(file_idx, line):
    if not line.startswith('#'):
        line = line.split('\t', maxsplit=9)
        if not line[8].endswith(':FT'):
            line[8] += ':FT'
            line[-1] = line[-1].rstrip() + ':' + line[6] + '\n'
            line[6] = '.'
        line = '\t'.join(line)
    return line


def strip_fixed_columns(file_idx, line):
    if not is_first_file(file_idx) and not is_header(line):
        line = line.split('\t', maxsplit=9)[-1]

    return line
