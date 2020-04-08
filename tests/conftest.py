import pytest

from ivcfmerge.utils.test.fixtures import sample_input_paths, reference_merged_path, reference_merged_single_input_path


@pytest.fixture
def ref_merged_path():
    return reference_merged_path()


@pytest.fixture
def ref_merged_single_input_path():
    return reference_merged_single_input_path()


# We need to call _input_paths directly sometimes, hence the explicit but different named fixture
input_paths = pytest.fixture(sample_input_paths)
