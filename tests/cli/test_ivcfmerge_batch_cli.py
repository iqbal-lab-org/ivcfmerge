import subprocess

from hypothesis import given, strategies as st


def test_merging_example_input(input_paths_file, ref_merged_path, tmp_path):
    output_path = tmp_path / 'out.vcf'

    subprocess.run(['python3', 'ivcfmerge_batch.py', input_paths_file, str(output_path)])

    with output_path.open() as outfile, open(ref_merged_path, 'r') as ref_merged:
        assert outfile.read() == ref_merged.read()


@given(batch_size=st.integers())
def test_batch_sizes(input_paths_file, ref_merged_path, tmp_path, batch_size):
    output_path = tmp_path / 'out.vcf'

    subprocess.run(['python3', 'ivcfmerge_batch.py', '--batch-size', str(batch_size), input_paths_file,
                    str(output_path)])

    with output_path.open() as outfile, open(ref_merged_path, 'r') as ref_merged:
        assert outfile.read() == ref_merged.read()


@given(batch_size=st.integers())
def test_temporary_dir(input_paths_file, ref_merged_path, tmp_path, batch_size):
    output_path = tmp_path / 'out.vcf'

    subprocess.run(['python3', 'ivcfmerge_batch.py', '--batch-size', str(batch_size),
                    '--temp-dir', str(tmp_path), input_paths_file, str(output_path)])

    with output_path.open() as outfile, open(ref_merged_path, 'r') as ref_merged:
        assert outfile.read() == ref_merged.read()
