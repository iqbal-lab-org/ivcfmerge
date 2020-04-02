from .utils import is_first_file, is_header, contains_field, add_field


def annotate_filter_values(file_idx, columns):
    if not columns[0].startswith('#') and not contains_field(columns[8], 'FT'):
        columns[8] = add_field(columns[8], 'FT')
        columns[-1] = add_field(columns[-1].rstrip(), columns[6]) + '\n'
        columns[6] = '.'
    return columns


def strip_fixed_columns(file_idx, columns):
    if not is_first_file(file_idx) and not is_header(columns[0]):
        columns = [columns[-1]]

    return columns
