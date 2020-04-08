import subprocess
import tempfile
from _signal import SIGTERM
from pathlib import Path
from unittest import mock

import pytest
from hypothesis import given, strategies as st

from ivcfmerge.utils.test.fixtures import sample_input_paths, sample_input_paths_file, reference_merged_path


def setup_func():
    input_paths_file = sample_input_paths_file()
    ref_merged_path = reference_merged_path()
    output_path = Path(tempfile.mkdtemp()) / 'out.vcf'
    temp_dir = tempfile.mkdtemp()

    return input_paths_file, ref_merged_path, output_path, temp_dir


def test_merging_example_input(input_paths_file, ref_merged_path, tmp_path):
    output_path = tmp_path / 'out.vcf'

    subprocess.run(['python3', 'ivcfmerge_batch.py', input_paths_file, str(output_path)])

    with output_path.open() as outfile, open(ref_merged_path, 'r') as ref_merged:
        assert outfile.read() == ref_merged.read()


@given(batch_size=st.integers())
def test_batch_sizes(batch_size):
    input_paths_file, ref_merged_path, output_path, _ = setup_func()

    subprocess.run(['python3', 'ivcfmerge_batch.py', '--batch-size', str(batch_size), input_paths_file,
                    str(output_path)])

    with output_path.open() as outfile, open(ref_merged_path, 'r') as ref_merged:
        assert outfile.read() == ref_merged.read()


@given(batch_size=st.integers())
def test_temporary_dir(batch_size):
    input_paths_file, ref_merged_path, output_path, temp_dir = setup_func()

    subprocess.run(['python3', 'ivcfmerge_batch.py', '--batch-size', str(batch_size),
                    '--temp-dir', str(temp_dir), input_paths_file, str(output_path)])

    with output_path.open() as outfile, open(ref_merged_path, 'r') as ref_merged:
        assert outfile.read() == ref_merged.read()


@given(batch_size=st.integers(min_value=2, max_value=len(sample_input_paths()) - 1))
def test_not_cleaning_up_temporary_directory_on_sigterm(batch_size):
    input_paths_file, _, output_path, temp_dir = setup_func()

    def write_file(temp_dir):
        open(Path(temp_dir) / 'random', 'w')

    with mock.patch('ivcfmerge.batch._ivcfmerge', side_effect=write_file(temp_dir)):
        process = subprocess.Popen(['python3', 'ivcfmerge_batch.py', '--batch-size', str(batch_size),
                                    '--temp-dir', str(temp_dir), input_paths_file, str(output_path)])
    process.send_signal(SIGTERM)
    process.wait()

    assert process.returncode != 0

    with pytest.raises(OSError):
        Path(temp_dir).rmdir()
