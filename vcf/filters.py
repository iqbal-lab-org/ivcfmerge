from vcf.utils import is_header, is_first_file


def not_subsequent_header(item):
    file_idx, line = item
    return is_first_file(file_idx) or not is_header(line)
