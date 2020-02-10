from .. import naive_paste_incremental

from multifile.reader.header_aware import HeaderAwareMultifileReader


class VCFPaster:
    def __init__(self, input_paths, output_path, delimeter='\t', batch_size=2, n_header_lines=11, n_fixed_cols=9, temp_dir_path=None, n_processes=1):
        self._input_paths = input_paths
        self._output_path = output_path
        self._delimeter = delimeter
        self._batch_size = batch_size
        self._n_header_lines = n_header_lines
        self._n_fixed_cols = n_fixed_cols
        self._temp_dir_path = temp_dir_path
        self._n_processes = n_processes

    def paste(self):
        reader = HeaderAwareMultifileReader(self._input_paths, n_header_lines=self._n_header_lines)

        return naive_paste_incremental(
            reader, self._output_path, self._delimeter, self._batch_size,
            cell_preprocessor=self._strip_fixed_cols_from_line, temp_dir_path=self._temp_dir_path,
            keep_input_order=False)

    def _strip_fixed_cols_from_line(self, line, metadata):
        if self._is_header_line(metadata['line_idx']) or self._is_first_file(metadata['file_idx']):
            return line

        cells = line.split(self._delimeter, maxsplit=self._n_fixed_cols)
        sample_cells = cells[self._n_fixed_cols:]

        new_line = self._delimeter.join(sample_cells)
        return new_line

    def _is_header_line(self, line_idx):
        return line_idx < self._n_header_lines

    def _is_first_file(self, file_idx):
        return file_idx == 0