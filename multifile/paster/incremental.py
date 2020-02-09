import shutil
import tempfile

from .naive import naive_paste


def naive_paste_incremental(reader, output_path, delimeter='', batch_size=999, cell_preprocessor=None, temp_dir_path=None, keep_input_order=True):
    if batch_size < 1:
        return

    if batch_size == 1 or batch_size >= len(reader.paths):
        naive_paste(reader, output_path, delimeter, cell_preprocessor)
        return

    start = 0
    original_input_paths = reader.paths

    previous_temp_output_file = tempfile.NamedTemporaryFile('r+', dir=temp_dir_path)
    while True:
        batch = original_input_paths[start : start + batch_size]
        if not batch:
            break

        temp_output_file = tempfile.NamedTemporaryFile('r+', dir=temp_dir_path)

        if start > 0:
            if keep_input_order:
                batch = [previous_temp_output_file.name] + batch
            else:
                batch.append(previous_temp_output_file.name)
        
        reader.paths = batch
        naive_paste(reader, temp_output_file.name, delimeter, cell_preprocessor)

        start += batch_size
        shutil.copyfile(temp_output_file.name, previous_temp_output_file.name)

    shutil.copyfile(previous_temp_output_file.name, output_path)

