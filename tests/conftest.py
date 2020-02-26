import pytest


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
