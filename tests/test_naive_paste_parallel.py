import os
import tempfile

from multifile.paster.parallel import naive_paste_parallel
from multifile.reader.plain import PlainMultifileReader


THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(THIS_SCRIPT_DIR, 'data')
REF_PARALLEL = os.path.join(TEST_DATA_DIR, 'ref_parallel.vcf')
REF_PARALLEL_IGNORE_ORDER = os.path.join(TEST_DATA_DIR, 'ref_parallel_ignore_order.vcf')


def test_naive_paste_parallel():
    test_files = ['ref_1.vcf', 'ref_2.vcf', 'ref_3.vcf', 'ref_4.vcf', 'ref_5.vcf', 'ref_6.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = PlainMultifileReader(input_paths)

    naive_paste_parallel(reader, output_file.name, n_processes=2)

    with open(REF_PARALLEL, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


def test_naive_paste_parallel_ignore_order():
    test_files = ['ref_1.vcf', 'ref_2.vcf', 'ref_3.vcf', 'ref_4.vcf', 'ref_5.vcf', 'ref_6.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = PlainMultifileReader(input_paths)

    naive_paste_parallel(reader, output_file.name, n_processes=2, keep_input_order=False)

    with open(REF_PARALLEL_IGNORE_ORDER, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()
