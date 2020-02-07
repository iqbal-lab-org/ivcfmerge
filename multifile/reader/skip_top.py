from .base import BaseMultifileReader


class SkipTopMultifileReader(BaseMultifileReader):
    def __init__(self, paths, from_line=0):
        super().__init__(paths)
        self._from_line = from_line

    def _should_read(self):
        return self._line_idx >= self._from_line