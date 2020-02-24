from contextlib import ExitStack
from tempfile import TemporaryFile

from ivcfmerge import ivcfmerge


def test_merging_example_input():
    input_paths = [
        'tests/data/input/1.vcf',
        'tests/data/input/2.vcf',
        'tests/data/input/3.vcf',
        'tests/data/input/4.vcf',
        'tests/data/input/5.vcf',
        'tests/data/input/6.vcf',
    ]
    ref_merged_path = 'tests/data/ref/merged.vcf'

    with ExitStack() as stack:
        files = map(lambda fn: stack.enter_context(open(fn)), input_paths)
        with TemporaryFile('w+') as outfile, open(ref_merged_path, 'r') as expected:
            ivcfmerge(files, outfile)

            outfile.seek(0)
            assert outfile.read() == expected.read()
