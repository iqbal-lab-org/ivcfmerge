from hypothesis import given, strategies as st

from ivcfmerge.transformers import strip_fixed_columns
from ivcfmerge.utils import split_columns
from tests.strategies import vcf_lines


@given(file_idx=st.just(0), line=st.text())
def test_first_file_is_unaffected(file_idx, line):
    assert strip_fixed_columns(file_idx, line) == line


@given(file_idx=st.integers(), line=st.from_regex('^##.*'))
def test_headers_are_unaffected(file_idx, line):
    cols = split_columns(line)
    assert strip_fixed_columns(file_idx, cols) == cols


@given(file_idx=st.integers(min_value=1), line=vcf_lines())
def test_stripping_fixed_columns(file_idx, line):
    cols = split_columns(line)
    assert strip_fixed_columns(file_idx, cols) == [cols[-1]]
