import os
import tempfile

from multifile.paster.vcf.paster import VCFPaster


THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(THIS_SCRIPT_DIR, 'data')
REF_FIXED_COLS = os.path.join(TEST_DATA_DIR, 'ref_fixed_cols.vcf')
REF_FIXED_COLS_NON_TRIVIAL = os.path.join(TEST_DATA_DIR, 'ref_fixed_cols_incremental.vcf')


def test_vcf_paste():
    test_files = ['ref_1.vcf', 'ref_2.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    paster = VCFPaster(input_paths, output_file.name)
    paster.paste()

    with open(REF_FIXED_COLS, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


def test_vcf_paste_non_trivial():
    test_files = ['ref_1.vcf', 'ref_2.vcf', 'ref_3.vcf', 'ref_4.vcf', 'ref_5.vcf', 'ref_6.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    paster = VCFPaster(input_paths, output_file.name)
    paster.paste()

    with open(REF_FIXED_COLS_NON_TRIVIAL, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


def test_vcf_paste_non_trivial_parallel():
    test_files = ['ref_1.vcf', 'ref_2.vcf', 'ref_3.vcf', 'ref_4.vcf', 'ref_5.vcf', 'ref_6.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    paster = VCFPaster(input_paths, output_file.name, n_processes=2)
    paster.paste()

    output = output_file.read()
    assert all([('%d' % i) in output for i in [1, 2, 4, 5, 6]])
