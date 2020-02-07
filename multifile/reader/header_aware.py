from .base import BaseMultifileReader


class HeaderAwareMultifileReader(BaseMultifileReader):
    def __init__(self, paths, n_header_lines=0):
        super().__init__(paths)
        self._n_header_lines = n_header_lines

    def _should_read(self):
        return not self._is_header() or self._is_first_file()

    def _sanitize(self, cell):
        if not self._is_last_file() and not self._is_header():
            cell = cell.rstrip('\n')
        return cell

    def _is_header(self):
        return self._line_idx < self._n_header_lines