from .base import BaseMultifileReader


class PlainMultifileReader(BaseMultifileReader):
    def _should_read(self):
        return True