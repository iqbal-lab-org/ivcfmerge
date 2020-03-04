from contextlib import ExitStack
from tempfile import TemporaryFile

from ivcfmerge import ivcfmerge


def test_merging_example_input(input_paths, ref_merged_path):
    with ExitStack() as stack:
        files = map(lambda fn: stack.enter_context(open(fn)), input_paths)
        with TemporaryFile('w+') as outfile, open(ref_merged_path, 'r') as expected:
            ivcfmerge(files, outfile)

            outfile.seek(0)
            assert outfile.read() == expected.read()


def test_single_input(ref_merged_single_input_path):
    input_path = 'tests/data/input/1.vcf'

    with ExitStack() as stack:
        files = map(lambda fn: stack.enter_context(open(fn)), [input_path])
        with TemporaryFile('w+') as outfile, open(ref_merged_single_input_path, 'r') as expected:
            ivcfmerge(files, outfile)

            outfile.seek(0)
            assert outfile.read() == expected.read()


def test_empty_input_list():
    input_paths = []

    with ExitStack() as stack:
        files = map(lambda fn: stack.enter_context(open(fn)), input_paths)
        with TemporaryFile('w+') as outfile:
            ivcfmerge(files, outfile)

            outfile.seek(0)
            assert outfile.read() == ''
