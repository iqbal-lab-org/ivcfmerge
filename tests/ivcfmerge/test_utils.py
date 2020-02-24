import itertools
import tempfile

from hypothesis import strategies as st, given

from ivcfmerge.utils import assign_file_index_to_lines, is_first_file, is_header, write_vcf


@given(file_idx=st.integers(), lines=st.iterables(elements=st.text()))
def test_assign_file_index_to_lines(file_idx, lines):
    lines_copy_1, lines_copy_2 = itertools.tee(lines)
    actual = assign_file_index_to_lines(file_idx, lines_copy_1)
    expected = [(file_idx, line) for line in lines_copy_2]

    for a, e in zip(actual, expected):
        assert a == e


def test_is_first_file():
    assert is_first_file(0)


@given(not_first_file_idx=st.integers(min_value=1))
def test_is_not_first_file(not_first_file_idx):
    assert not is_first_file(not_first_file_idx)


@given(header=st.from_regex('^##.*'))
def test_any_string_begins_with_double_sharp_is_considered_a_vcf_header(header):
    assert is_header(header)


@given(header=st.from_regex('^(?!##).*'))
def test_any_string_does_not_begin_with_double_sharp_is_not_considered_a_vcf_header(header):
    assert not is_header(header)


def test_write_vcf_utility_replaces_new_lines_with_tabs_for_data_lines_of_all_but_last_file():
    lines = [
        (0, '##header\n'),
        (0, '##header\n'),
        (0, 'data\n'),
        (1, 'data\n'),
        (0, 'data\n'),
        (1, 'data\n'),
    ]
    n_input_files = 2
    expected = "##header\n##header\ndata\tdata\ndata\tdata\n"

    with tempfile.TemporaryFile('r+') as f:
        write_vcf(lines, f, n_input_files)

        f.seek(0)
        assert f.read() == expected