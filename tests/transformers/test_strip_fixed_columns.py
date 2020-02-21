from hypothesis import given, strategies as st

from vcf.transformers import strip_fixed_columns


@given(file_idx=st.just(0), line=st.text())
def test_first_file_is_unaffected(file_idx, line):
    assert strip_fixed_columns(file_idx, line) == line


@given(file_idx=st.integers(), line=st.from_regex('^##.*'))
def test_headers_are_unaffected(file_idx, line):
    assert strip_fixed_columns(file_idx, line) == line


@given(file_idx=st.integers(min_value=1), line=st.from_regex('^([^\t]+\t){8}[^\t]+$'))
def test_stripping_8_fixed_columns(file_idx, line):
    assert strip_fixed_columns(file_idx, line) == line.split('\t')[8]


@given(file_idx=st.integers(min_value=1), line=st.from_regex('^([^\t]+\t){9}[^\t]+$'))
def test_stripping_9_fixed_columns(file_idx, line):
    assert strip_fixed_columns(file_idx, line) == line.split('\t')[9]
