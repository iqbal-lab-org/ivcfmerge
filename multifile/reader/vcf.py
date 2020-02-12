from .base import MultifileReader


N_FIXED_COLUMNS = 9


class MultiVCFReader(MultifileReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._headers = []
        self._chrom_pos = []

    def __next__(self):
        line = super().__next__()

        if line.startswith('##'):
            if line not in self._headers:
                self._headers.append(line)
            else:
                line = ''
        else:
            cells = line.split('\t', maxsplit=N_FIXED_COLUMNS)
            chrom_pos = '-'.join(cells[:2])
            if chrom_pos in self._chrom_pos:
                line = cells[-1]
            else:
                self._chrom_pos.append(chrom_pos)

        return line
