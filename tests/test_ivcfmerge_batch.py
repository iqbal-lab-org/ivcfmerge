import tempfile
from contextlib import ExitStack
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryFile
from unittest import mock

import pytest
from hypothesis import given, strategies as st

from ivcfmerge import ivcfmerge_batch, ivcfmerge
from ivcfmerge.utils.test.fixtures import sample_input_paths, reference_merged_path


def setup_func():
    input_paths = sample_input_paths()
    ref_merged_path = reference_merged_path()
    temp_dir = tempfile.mkdtemp()

    return input_paths, ref_merged_path, temp_dir


@given(batch_size=st.integers(min_value=2))
def test_merging_example_input(batch_size):
    input_paths, ref_merged_path, _ = setup_func()

    with NamedTemporaryFile('w+') as outfile, open(ref_merged_path, 'r') as ref_merged:
        ivcfmerge_batch(input_paths, outfile.name, batch_size)
        output = outfile.read()

        assert output == ref_merged.read()


@given(batch_size=st.one_of(
    st.integers(max_value=1),
    st.integers(min_value=len(sample_input_paths()))
))
def test_out_of_bound_batch_sizes_yield_the_same_output_as_normal_ivcfmerge(batch_size):
    input_paths, _, _ = setup_func()

    with ExitStack() as stack:
        files = map(lambda fn: stack.enter_context(open(fn)), input_paths)
        with TemporaryFile('w+') as outfile:
            ivcfmerge(files, outfile)
            outfile.seek(0)
            expected = outfile.read()

    with NamedTemporaryFile('w+') as outfile:
        ivcfmerge_batch(input_paths, outfile.name, batch_size)
        output = outfile.read()

    assert output == expected


@given(batch_size=st.integers())
def test_single_input_yields_the_same_output_as_normal_ivcfmerge(batch_size):
    input_paths = ['tests/data/input/1.vcf']

    with ExitStack() as stack:
        files = map(lambda fn: stack.enter_context(open(fn)), input_paths)
        with TemporaryFile('w+') as outfile:
            ivcfmerge(files, outfile)
            outfile.seek(0)
            expected = outfile.read()

    with NamedTemporaryFile('w+') as outfile:
        ivcfmerge_batch(input_paths, outfile.name, batch_size)
        output = outfile.read()

    assert output == expected


@given(batch_size=st.integers())
def test_custom_temporary_directory(batch_size):
    input_paths, ref_merged_path, temp_dir = setup_func()

    with NamedTemporaryFile('w+') as outfile, open(ref_merged_path, 'r') as ref_merged:
        ivcfmerge_batch(input_paths, outfile.name, batch_size, temp_dir)
        output = outfile.read()

        assert output == ref_merged.read()


@given(batch_size=st.integers(min_value=2, max_value=len(sample_input_paths()) - 1))
def test_cleaning_up_temporary_files(batch_size):
    input_paths, _, temp_dir = setup_func()

    with NamedTemporaryFile('w+') as outfile:
        ivcfmerge_batch(input_paths, outfile.name, batch_size, temp_dir)

    # Will throw exception if not empty
    Path(temp_dir).rmdir()


@given(batch_size=st.integers(min_value=2, max_value=len(sample_input_paths()) - 1))
def test_not_cleaning_up_other_files(batch_size):
    input_paths, _, temp_dir = setup_func()
    (Path(temp_dir) / 'other').touch()

    with NamedTemporaryFile('w+') as outfile:
        ivcfmerge_batch(input_paths, outfile.name, batch_size, temp_dir)

    with pytest.raises(OSError):
        Path(temp_dir).rmdir()


@given(batch_size=st.integers(min_value=2, max_value=len(sample_input_paths()) - 1))
def test_not_cleaning_up_temporary_directory_in_failures(batch_size):
    input_paths, _, temp_dir = setup_func()

    expected_error = Exception

    def write_file(temp_dir):
        open(Path(temp_dir) / 'random', 'w')

    with mock.patch('ivcfmerge.batch._ivcfmerge', side_effect=[write_file(temp_dir), expected_error]),\
            NamedTemporaryFile('w+') as outfile, pytest.raises(expected_error):
        ivcfmerge_batch(input_paths, outfile.name, batch_size, temp_dir)

    with pytest.raises(OSError):
        Path(temp_dir).rmdir()
