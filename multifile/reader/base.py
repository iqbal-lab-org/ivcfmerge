import itertools


class BaseMultifileReader:
    """A base class to read multiple files horizontally.

    It spits out the 1st line of the 1st file, then that of the 2nd file, until the last file,
    then come back and splits out the 1nd line of the 1st file, and so on.
    """

    def __init__(self, paths):
        self._paths = paths
        self._n_files = len(self._paths)

    def __enter__(self):
        self._files = [open(p, 'r') for p in self._paths]
        self._files_cycle = itertools.cycle(enumerate(self._files))

        self._line_idx = 0

        return self

    def __exit__(self, *args, **kwargs):
        [f.close() for f in self._files]

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._cell_by_cell()
        except AttributeError:
            raise Exception("Files not opened. Open files by creating the reader in a 'with' statement.")

    def _cell_by_cell(self):
        self._file_idx, f = next(self._files_cycle)

        # TODO: if should_stop() then raise StopIteration

        if not self._should_read():
            next(f)
            cell = None
            metadata = None
        else:
            # Attempt to read a line
            cell = f.readline()
            if not cell:
                raise StopIteration

            cell = self._sanitize(cell)

            metadata = {
                'file_idx': self._file_idx,
                'line_idx': self._line_idx,
            }

        self._track_current_line()

        return cell, metadata

    def _sanitize(self, cell):
        if not self._is_last_file():
            cell = cell.rstrip('\n')
        return cell

    def _is_first_file(self):
        return self._file_idx == 0

    def _is_last_file(self):
        return self._file_idx == self._n_files - 1

    def _track_current_line(self):
        if self._is_last_file():
            self._line_idx += 1

    def _should_read(self):
        raise NotImplementedError
