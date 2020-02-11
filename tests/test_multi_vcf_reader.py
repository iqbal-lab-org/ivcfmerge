import itertools
import os
import pytest

from multifile.reader import MultiVCFReader, BadUsageError


@pytest.fixture
def ref_data():
    this_script_dir = os.path.dirname(os.path.realpath(__file__))
    test_data_dir = os.path.join(this_script_dir, 'data')

    input_filenames = ['ref_%d.vcf' % i for i in range(1, 7)]

    return {
        'input_paths': [os.path.join(test_data_dir, filename) for filename in input_filenames]
    }


@pytest.fixture
def expected_lines(ref_data):
    files = itertools.cycle(map(lambda p: open(p, 'r'), ref_data['input_paths']))
    def lines_iterator(f):
        line = f.readline()
        if not line:
            raise StopIteration
        return line.rstrip()
    return map(lines_iterator, files)


@pytest.fixture
def expected_headers(expected_lines):
    headers = []

    for line in expected_lines:
        if line.startswith('##') and line not in headers:
            headers.append(line)

    return headers


def test_reader_implements_context_manager_protocol(ref_data):
    with MultiVCFReader(ref_data['input_paths']) as reader:
        pass


def test_reader_implements_iteration_protocol(ref_data):
    with MultiVCFReader(ref_data['input_paths']) as reader:
        next(reader)


def test_reader_can_be_iterated_in_for_loops(ref_data):
    with MultiVCFReader(ref_data['input_paths']) as reader:
        for _ in reader:
            pass


def test_reader_forces_using_context_manager_before_iterating(ref_data):
    with pytest.raises(BadUsageError):
        reader = MultiVCFReader(ref_data['input_paths'])
        next(reader)


def test_iterating_reader_yields_lines_in_correct_order(ref_data, expected_lines):
    with MultiVCFReader(ref_data['input_paths']) as reader:
        for line in expected_lines:
            assert next(reader) == line


def test_reader_terminates_on_end_of_input(ref_data, expected_lines):
    with MultiVCFReader(ref_data['input_paths']) as reader:
        for _ in expected_lines:
            next(reader)

        with pytest.raises(StopIteration):
            next(reader)


def test_read_lines_are_trimmed_of_their_original_newlines(ref_data, expected_lines):
    with MultiVCFReader(ref_data['input_paths']) as reader:
        for line in reader:
            assert not line.endswith('\n')


def test_reader_closes_files_on_exit(ref_data, mocker):
    n_files = len(ref_data['input_paths'])
    mocked_files = [mocker.MagicMock() for _ in range(n_files)]

    with MultiVCFReader(ref_data['input_paths']) as reader:
        mocker.patch.object(reader, '_files', new=mocked_files)

    [f.close.assert_called() for f in mocked_files]


def test_reader_collects_headers(ref_data, expected_headers):
    with MultiVCFReader(ref_data['input_paths']) as reader:
        for _ in reader:
            pass

        assert reader.headers == expected_headers
