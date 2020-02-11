import itertools
from warnings import warn


class MultiVCFReader:
    def __init__(self, input_paths):
        self._input_paths = input_paths
        self.headers = []
        self.samples = set()

    def __enter__(self):
        files = map(lambda p: open(p, 'r'), self._input_paths)
        self._files = self._filter_valid_vcf_files(files)
        self._file_cycle = itertools.cycle(self._files)

        return self

    def __exit__(self, *args, **kwargs):
        [f.close() for f in self._files]

    def __next__(self):
        if not getattr(self, '_files', None):
            raise BadUsageError

        line = next(self._file_cycle).readline()
        if not line:
            raise StopIteration

        line = line.rstrip()

        if line.startswith('##'):
            if line not in self.headers:
                self.headers.append(line)
            else:
                line = ''
        elif line.startswith('#'):
            parts = line.split('FORMAT\t', maxsplit=1)
            if len(parts) > 1:
                samples_in_line = parts[1].split('\t')
                self.samples.update(samples_in_line)

        return line

    def __iter__(self):
        return self

    def _filter_valid_vcf_files(self, files):
        def is_valid(f):
            line = f.readline()
            f.seek(0)

            is_valid = line.startswith('##fileformat=VCF')
            if not is_valid:
                warn(InvalidFileWarning(f.name, "##fileformat=VCF... header not found"))

            return is_valid
        
        return filter(is_valid, files)


class BadUsageError(Exception):
    def __str__(self):
        return "MultiVCFReader should be used inside a context manager"


class InvalidFileWarning(UserWarning):
    def __init__(self, path, reason):
        self._path = path
        self._reason = reason

    def __str__(self):
        return "file %s is not a valid VCF. Reason: %s" % (self._path, self._reason)
