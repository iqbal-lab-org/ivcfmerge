import os
import tempfile

from multifile.paster.naive import naive_paste
from multifile.reader.skip_top import SkipTopMultifileReader
from multifile.reader.plain import PlainMultifileReader
from multifile.reader.header_aware import HeaderAwareMultifileReader


THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(THIS_SCRIPT_DIR, 'data')
REF_MERGED_FILE = os.path.join(TEST_DATA_DIR, 'ref_merged.vcf')
REF_SKIPPED_HEADERS = os.path.join(TEST_DATA_DIR, 'ref_skipped_headers.vcf')
REF_PROPER_HEADERS = os.path.join(TEST_DATA_DIR, 'ref_proper_headers.vcf')
REF_STRIPPED_COLS = os.path.join(TEST_DATA_DIR, 'ref_stripped_cols.vcf')


def test_naive_paste():
    test_files = ['ref_1.vcf', 'ref_2.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = PlainMultifileReader(input_paths)

    naive_paste(reader, output_file.name)

    with open(REF_MERGED_FILE, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


def test_naive_paste_with_one_input_file():
    test_file = os.path.join(TEST_DATA_DIR, 'ref_1.vcf')
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = PlainMultifileReader([test_file])

    naive_paste(reader, output_file.name)

    with open(test_file, 'r') as input_file:
        assert output_file.read() == input_file.read()


def test_naive_paste_skipped_headers():
    test_files = ['ref_1.vcf', 'ref_2.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = SkipTopMultifileReader(input_paths, from_line=11)

    naive_paste(reader, output_file.name)

    with open(REF_SKIPPED_HEADERS, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


def test_naive_paste_proper_headers():
    test_files = ['ref_1.vcf', 'ref_2.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = HeaderAwareMultifileReader(input_paths, n_header_lines=11)

    naive_paste(reader, output_file.name)

    with open(REF_PROPER_HEADERS, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


# def test_naive_paste_cell_preprocessor():
#     test_files = ['ref_1.vcf', 'ref_2.vcf']
#     input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
#     output_file = tempfile.NamedTemporaryFile(mode='r+')

#     def fn(cell, metadata):
#         return cell.rsplit('\t', maxsplit=1)[1]

#     naive_paste(input_paths, output_file.name, from_line=11, cell_preprocessor=fn)

#     with open(REF_STRIPPED_COLS, 'r') as ref_merged:
#         assert output_file.read() == ref_merged.read()