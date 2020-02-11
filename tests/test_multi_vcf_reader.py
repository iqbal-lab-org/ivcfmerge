import os
import pytest

from multifile.reader import MultiVCFReader


@pytest.fixture
def ref_data():
    this_script_dir = os.path.dirname(os.path.realpath(__file__))
    test_data_dir = os.path.join(this_script_dir, 'data')

    input_filenames = ['ref_%d.vcf' % i for i in range(6)]

    return {
        'input_paths': [os.path.join(test_data_dir, filename) for filename in input_filenames]
    }


def test_reader_implements_context_manager_protocol(ref_data):
    with MultiVCFReader(ref_data['input_paths']) as reader:
        pass


def test_reader_implements_iteration_protocol(ref_data):
    reader = MultiVCFReader(ref_data['input_paths'])
    next(reader)
