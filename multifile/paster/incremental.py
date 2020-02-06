import shutil
import tempfile

from .naive import naive_paste


def naive_paste_incremental(input_paths, output_path, delimeter='', batch_size=999, from_line=0, n_header_lines=0, cell_preprocessor=None):
    if batch_size < 1:
        return

    if batch_size == 1 or batch_size >= len(input_paths):
        naive_paste(input_paths, output_path, delimeter, from_line, n_header_lines, cell_preprocessor)
        return

    start = 0

    previous_temp_output_file = tempfile.NamedTemporaryFile('r+')
    while True:
        batch = input_paths[start : start + batch_size]
        if not batch:
            break

        temp_output_file = tempfile.NamedTemporaryFile('r+')

        if start > 0:
            batch = [previous_temp_output_file.name] + batch
        
        naive_paste(batch, temp_output_file.name, delimeter, from_line, n_header_lines, cell_preprocessor)

        start += batch_size
        shutil.copyfile(temp_output_file.name, previous_temp_output_file.name)

    shutil.copyfile(previous_temp_output_file.name, output_path)

