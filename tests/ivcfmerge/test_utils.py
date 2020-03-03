import itertools
import re
import tempfile

from hypothesis import strategies as st, given, example

from ivcfmerge.utils import assign_file_index_to_lines, is_first_file, is_header, write_vcf, split_columns, \
    contains_field
from tests.strategies import vcf_lines


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
@example(header='#C')
def test_any_string_does_not_begin_with_double_sharp_is_not_considered_a_vcf_header(header):
    assert not is_header(header)


@given(line=vcf_lines())
def test_split_columns(line):
    assert split_columns(line) == line.split('\t', maxsplit=9)


@given(st.data())
def test_contains_field(data):
    field = data.draw(st.text())
    column = data.draw(st.one_of(
        st.from_regex(':%s' % re.escape(field)),
        st.from_regex('%s:' % re.escape(field))
    ))

    assert contains_field(column, field)


@given(st.data())
def test_not_contain_field(data):
    field = data.draw(st.text())
    column = data.draw(st.from_regex('(?!%s)' % re.escape(field)))

    assert not contains_field(column, field)


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
