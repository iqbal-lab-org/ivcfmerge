import itertools


class MultifileReader:
    def __init__(self, input_paths):
        self._input_paths = input_paths

    def __enter__(self):
        self._files = map(lambda p: open(p, 'r'), self._input_paths)
        self._file_cycle = itertools.cycle(self._files)

        return self

    def __exit__(self, *args, **kwargs):
        [f.close() for f in self._files]

    def __next__(self):
        if not getattr(self, '_file_cycle', None):
            raise BadUsageError

        line = next(self._file_cycle).readline()
        if not line:
            raise StopIteration

        return line.rstrip()

    def __iter__(self):
        return self


class BadUsageError(Exception):
    def __str__(self):
        return "Multifile readers should be used inside context managers"
