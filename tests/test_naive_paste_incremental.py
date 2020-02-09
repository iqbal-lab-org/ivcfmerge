import os
import tempfile

from hypothesis import given, strategies as st

from multifile.paster.incremental import naive_paste_incremental
from multifile.reader.plain import PlainMultifileReader


THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(THIS_SCRIPT_DIR, 'data')
REF_MERGED_FILE = os.path.join(TEST_DATA_DIR, 'ref_merged.vcf')
REF_BATCH_MERGED_FILE = os.path.join(TEST_DATA_DIR, 'ref_batch_merged.vcf')
REF_3412_FILE = os.path.join(TEST_DATA_DIR, 'ref_batch_merged_3412.vcf')
REF_4123_FILE = os.path.join(TEST_DATA_DIR, 'ref_batch_merged_4123.vcf')


@given(batch_size=st.integers(max_value=0))
def test_naive_paste_incremental_batch_size_less_than_one(batch_size):
    test_files = ['ref_1.vcf', 'ref_2.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = PlainMultifileReader(input_paths)
    
    naive_paste_incremental(reader, output_file.name, batch_size=batch_size)

    assert output_file.read() == ''


def test_naive_paste_incremental_batch_size_one():
    test_files = ['ref_1.vcf', 'ref_2.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = PlainMultifileReader(input_paths)
    
    naive_paste_incremental(reader, output_file.name, batch_size=1)

    with open(REF_MERGED_FILE, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


@given(pool=st.data())
def test_naive_paste_incremental_one_batch(pool):
    test_files = ['ref_1.vcf', 'ref_2.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')
    batch_size = pool.draw(st.integers(min_value=len(input_paths)))

    reader = PlainMultifileReader(input_paths)
    
    naive_paste_incremental(reader, output_file.name, batch_size=batch_size)

    with open(REF_MERGED_FILE, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


@given(batch_size=st.integers(min_value=2, max_value=3))
def test_naive_paste_incremental(batch_size):
    test_files = ['ref_1.vcf', 'ref_2.vcf', 'ref_3.vcf', 'ref_4.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = PlainMultifileReader(input_paths)
    
    naive_paste_incremental(reader, output_file.name, batch_size=batch_size)

    with open(REF_BATCH_MERGED_FILE, 'r') as ref_merged:
        assert output_file.read() == ref_merged.read()


@given(batch_size=st.integers(min_value=2, max_value=3))
def test_naive_paste_incremental_ignore_input_order(batch_size):
    test_files = ['ref_1.vcf', 'ref_2.vcf', 'ref_3.vcf', 'ref_4.vcf']
    input_paths = [os.path.join(TEST_DATA_DIR, filename) for filename in test_files]
    output_file = tempfile.NamedTemporaryFile(mode='r+')

    reader = PlainMultifileReader(input_paths)
    
    naive_paste_incremental(reader, output_file.name, batch_size=batch_size, keep_input_order=False)

    if batch_size == 2:
        with open(REF_BATCH_MERGED_FILE, 'r') as ref_merged:
            assert output_file.read() == ref_merged.read()
    elif batch_size == 3:
        with open(REF_4123_FILE, 'r') as ref_merged:
            assert output_file.read() == ref_merged.read()