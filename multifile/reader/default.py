from .base import BaseMultifileReader


class DefaultMultifileReader(BaseMultifileReader):
    def __init__(self, paths, from_line=0, n_header_lines=0):
        super().__init__(paths)
        self._from_line = from_line
        self._n_header_lines = n_header_lines

    def _should_read(self):
        if self._from_line <= 0:
            should_read = not self._is_header() or self._is_first_file()
        else:
            should_read = self._line_idx >= self._from_line
        
        return should_read

    def _sanitize(self, cell):
        if not self._is_last_file() and not self._is_header():
            cell = cell.rstrip('\n')
        return cell

    def _is_header(self):
        return self._line_idx < self._n_header_lines