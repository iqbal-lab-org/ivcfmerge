from hypothesis import given, strategies as st

from ivcfmerge.transformers import annotate_filter_values
from ivcfmerge.utils import split_columns
from ivcfmerge.utils.test.strategies import vcf_lines


@given(file_idx=st.integers(), line=st.from_regex('^##'))
def test_ignore_headers(file_idx, line):
    assert annotate_filter_values(file_idx, line) == line


@given(file_idx=st.integers(), line=st.from_regex('^#'))
def test_ignore_column_names(file_idx, line):
    assert annotate_filter_values(file_idx, line) == line


@given(file_idx=st.integers(), line=vcf_lines())
def test_annotate_filter_values(file_idx, line):
    cols = split_columns(line)
    annotated = annotate_filter_values(file_idx, cols)

    line = line.split('\t', maxsplit=9)
    line[8] += ':FT'
    line[-1] = line[-1].rstrip() + ':' + line[6] + '\n'
    line[6] = '.'

    assert annotated == line
