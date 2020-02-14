import itertools


class MultiVCFReader:
    def __init__(self, input_paths):
        self._input_paths = input_paths

    def __enter__(self):
        self._files = map(lambda p: open(p, 'r'), self._input_paths)
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

        if file_idx < len(self._input_paths) - 1:
            delimiter = '\t'
        else:
            delimiter = '\n'

        return line + delimiter

    def __iter__(self):
        return self


class BadUsageError(Exception):
    def __str__(self):
        return "multifile readers should be used inside context managers"


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_paths', type=str, nargs='+')
    parser.add_argument('output_path', type=str)
    args = parser.parse_args()

    with open(args.output_path, 'w') as out_file:
        with MultiVCFReader(args.input_paths) as reader:
            for line in reader:
                out_file.write(line)
