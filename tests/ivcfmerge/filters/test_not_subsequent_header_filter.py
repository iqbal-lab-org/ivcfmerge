from hypothesis import given, strategies as st

from ivcfmerge.filters import not_subsequent_header


@given(file_idx=st.just(0), line=st.text())
def test_any_line_from_first_file_is_not_subsequent_header(file_idx, line):
    assert not_subsequent_header((file_idx, line))


@given(file_idx=st.integers(min_value=1), line=st.from_regex('^[^#].*$'))
def test_data_lines_from_subsequent_files_are_not_subsequent_headers(file_idx, line):
    assert not_subsequent_header((file_idx, line))


@given(file_idx=st.integers(min_value=1), line=st.from_regex('^#[^#].*$'))
def test_column_name_line_from_subsequent_files_is_not_subsequent_header(file_idx, line):
    assert not_subsequent_header((file_idx, line))


@given(file_idx=st.integers(min_value=1), line=st.from_regex('^##.*$'))
def test_lines_begin_with_double_sharp_from_subsequent_files_are_subsequent_header(file_idx, line):
    assert not not_subsequent_header((file_idx, line))
