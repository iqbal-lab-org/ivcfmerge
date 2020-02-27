import subprocess


def test_merging_example_input(input_paths_file, ref_merged_path, tmp_path):
    output_path = tmp_path / 'out.vcf'

    subprocess.run(['python', 'ivcfmerge.py', input_paths_file, str(output_path)])

    with output_path.open() as outfile, open(ref_merged_path, 'r') as ref_merged:
        assert outfile.read() == ref_merged.read()
