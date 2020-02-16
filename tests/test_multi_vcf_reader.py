import pytest

from vcf.reader import MultiVCFReader, BadUsageError


def test_reader_implements_context_manager_protocol(input_paths):
    with MultiVCFReader(input_paths):
        pass

    reader = MultiVCFReader(input_paths)
    with reader:
        pass


def test_reader_implements_iteration_protocol(input_paths):
    with MultiVCFReader(input_paths) as reader:
        next(reader)


def test_reader_can_be_iterated_in_for_loops(input_paths):
    with MultiVCFReader(input_paths) as reader:
        for _ in reader:
            pass


def test_reader_forces_using_context_manager_before_iterating(input_paths):
    with pytest.raises(BadUsageError):
        reader = MultiVCFReader(input_paths)
        next(reader)


def test_final_output(input_paths, ref_merged):
    with MultiVCFReader(input_paths) as reader:
        assert ''.join(reader) == ''.join(open(ref_merged, 'r'))


def test_reader_terminates_on_end_of_input(input_paths):
    with MultiVCFReader(input_paths) as reader:
        for _ in reader:
            pass

        with pytest.raises(StopIteration):
            next(reader)


def test_reader_closes_files_on_exit(input_paths, mocker):
    n_files = len(input_paths)
    mocked_files = [mocker.MagicMock() for _ in range(n_files)]

    with MultiVCFReader(input_paths) as reader:
        mocker.patch.object(reader, '_files', new=mocked_files)

    [f.close.assert_called() for f in mocked_files]


def test_reader_opens_and_closes_each_file_only_once(input_paths, mocker):
    n_files = len(input_paths)
    mocked_files = [mocker.MagicMock() for _ in range(n_files)]
    mocked_open = mocker.mock_open(read_data='a')
    mocker.patch('vcf.reader.open', mocked_open)

    with MultiVCFReader(input_paths) as reader:
        mocker.patch.object(reader, '_files', new=mocked_files)
        for _ in reader:
            pass

    assert mocked_open.call_count == n_files
    mocked_open.assert_has_calls([
        mocker.call(p, 'r') for p in input_paths
    ], any_order=True)
    [f.close.assert_called_once() for f in mocked_files]
