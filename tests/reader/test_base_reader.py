import itertools
from pathlib import Path
import pytest

from multifile.reader.base import MultifileReader, BadUsageError


def test_reader_implements_context_manager_protocol(input_paths):
    with MultifileReader(input_paths) as reader:
        pass

    reader = MultifileReader(input_paths)
    with reader:
        pass


def test_reader_implements_iteration_protocol(input_paths):
    with MultifileReader(input_paths) as reader:
        next(reader)


def test_reader_can_be_iterated_in_for_loops(input_paths):
    with MultifileReader(input_paths) as reader:
        for _ in reader:
            pass


def test_reader_forces_using_context_manager_before_iterating(input_paths):
    with pytest.raises(BadUsageError):
        reader = MultifileReader(input_paths)
        next(reader)


def test_reader_produces_equivalent_output_to_zipping_content_of_input_files(input_paths):
    input_files = [open(p, 'r') for p in input_paths]
    all_lines = [list(f) for f in input_files]  # [[all lines of file 1], [all lines of files 2], ...]
    combined_lines = zip(*all_lines)            # [(all 1st lines), (all 2nd lines), ...]
    flatten = itertools.chain(*combined_lines)
    stripped = [l.rstrip() for l in flatten]

    with MultifileReader(input_paths) as reader:
        assert list(reader) == list(stripped)


def test_read_lines_are_trimmed_of_their_original_newlines(input_paths):
    with MultifileReader(input_paths) as reader:
        for line in reader:
            assert not line.endswith('\n')


def test_reader_terminates_on_end_of_input(input_paths):
    with MultifileReader(input_paths) as reader:
        for _ in reader:
            pass

        with pytest.raises(StopIteration):
            next(reader)


def test_reader_closes_files_on_exit(input_paths, mocker):
    n_files = len(input_paths)
    mocked_files = [mocker.MagicMock() for _ in range(n_files)]

    with MultifileReader(input_paths) as reader:
        mocker.patch.object(reader, '_files', new=mocked_files)

    [f.close.assert_called() for f in mocked_files]
