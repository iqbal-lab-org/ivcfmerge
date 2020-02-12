import pytest

from multifile.reader.vcf import MultiVCFReader


def test_subsequent_headers_are_discarded(input_paths):
    headers = []
    first_file = open(input_paths[0], 'r')
    for line in first_file:
        if not line.startswith('##'):
            break
        headers.append(line.rstrip())

    with MultiVCFReader(input_paths) as reader:
        output = ''.join(reader)

        for header in headers:
            assert output.count(header) == 1


def test_subsequent_fixed_columns_are_discarded(input_paths):
    fixed = []
    first_file = open(input_paths[0], 'r')
    for line in first_file:
        if line.startswith('##'):
            continue
        line = line.split('\t', maxsplit=9)
        line = '\t'.join(line[:9])
        fixed.append(line)

    with MultiVCFReader(input_paths) as reader:
        output = ''.join(reader)

        for line in fixed:
            assert output.count(line) == 1


# def test_reader_skips_invalid_files(ref_data):
#     input_paths = ref_data['input_paths'][:]
#     input_paths.insert(int(len(input_paths)/2), ref_data['invalid'])

#     with MultiVCFReader(input_paths) as reader:
#         for _ in reader:
#             pass

#         assert 'invalid_sample_name' not in reader.samples


# def test_reader_warns_about_invalid_files(ref_data):
#     input_paths = ref_data['input_paths'][:]
#     input_paths.insert(int(len(input_paths)/2), ref_data['invalid'])

#     with pytest.warns(InvalidFileWarning):
#         with MultiVCFReader(input_paths) as reader:
#             pass


# def test_reader_outputs_headers_only_once(ref_data, expected_headers):
#     with MultiVCFReader(ref_data['input_paths']) as reader:
#         output = ''.join(reader)

#         assert all([output.count(h) == 1 for h in expected_headers])
