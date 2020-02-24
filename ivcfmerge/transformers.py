from .utils import is_first_file, is_header


def strip_fixed_columns(file_idx, line):
    if not is_first_file(file_idx) and not is_header(line):
        line = line.split('\t', maxsplit=9)[-1]

    return line
