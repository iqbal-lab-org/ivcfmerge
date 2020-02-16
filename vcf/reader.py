import itertools


class MultiVCFReader:
    def __init__(self, input_paths):
        self._input_paths = input_paths

    def __enter__(self):
        self._files = [open(p, 'r') for p in self._input_paths]
        self._file_cycle = itertools.cycle(enumerate(self._files))

        return self

    def __exit__(self, *args, **kwargs):
        [f.close() for f in self._files]

    def __next__(self):
        if not getattr(self, '_file_cycle', None):
            raise BadUsageError

        file_idx, file = next(self._file_cycle)

        line = file.readline()
        if not line:
            raise StopIteration
        
        line = line.rstrip()

        if file_idx > 0:
            if line.startswith('##'):
                line = ''
            else:
                line = line.split('\t', maxsplit=9)[-1]

        if file_idx < len(self._files) - 1:
            delimiter = '\t'
        else:
            delimiter = '\n'

        return line + delimiter

    def __iter__(self):
        return self


class BadUsageError(Exception):
    def __str__(self):
        return "multifile readers should be used inside context managers"
