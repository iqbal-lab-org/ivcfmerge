import itertools


class MultiVCFReader:
    def __init__(self, input_paths):
        self._input_paths = input_paths

    def __enter__(self):
        self._files = itertools.cycle(map(lambda p: open(p, 'r'), self._input_paths))
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __next__(self):
        if not getattr(self, '_files', None):
            raise BadUsageError

        return next(self._files).readline()


class BadUsageError(Exception):
    message = "Multi VCF reader should be used inside a context manager"
