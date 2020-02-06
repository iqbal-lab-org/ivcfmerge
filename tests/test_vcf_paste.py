import os
import tempfile

from multifile.paster.vcf.paster import VCFPaster


THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(THIS_SCRIPT_DIR, 'data')
REF_FIXED_COLS = os.path.join(TEST_DATA_DIR, 'ref_fixed_cols.vcf')


def test_vcf_paste():
    test_files = ['ref_1.vcf', 'ref_2.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    paster = VCFPaster(input_paths, output_file.name)
    paster.paste()

    with open(REF_FIXED_COLS, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()
