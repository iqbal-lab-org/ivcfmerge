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
