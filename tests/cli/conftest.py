import pytest

from ivcfmerge.utils.test.fixtures import sample_input_paths_file


@pytest.fixture
def input_paths_file():
    return sample_input_paths_file()
