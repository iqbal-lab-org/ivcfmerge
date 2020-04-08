import pytest

from ivcfmerge.utils.test.fixtures import sample_input_paths


@pytest.fixture
def ref_merged_path():
    return 'tests/data/ref/merged.vcf'


@pytest.fixture
def ref_merged_single_input_path():
    return 'tests/data/ref/merged_single_input.vcf'


# We need to call _input_paths directly sometimes, hence the explicit but different named fixture
input_paths = pytest.fixture(sample_input_paths)
