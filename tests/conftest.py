import pytest


@pytest.fixture
def ref_merged_path():
    return 'tests/data/ref/merged.vcf'


@pytest.fixture
def ref_merged_single_input_path():
    return 'tests/data/ref/merged_single_input.vcf'


def _input_paths():
    return [
        'tests/data/input/1.vcf',
        'tests/data/input/2.vcf',
        'tests/data/input/3.vcf',
        'tests/data/input/4.vcf',
        'tests/data/input/5.vcf',
        'tests/data/input/6.vcf',
    ]


# We need to call _input_paths directly sometimes, hence the explicit but different named fixture
input_paths = pytest.fixture(_input_paths)
