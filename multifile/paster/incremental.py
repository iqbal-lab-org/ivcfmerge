import os
import shutil
import tempfile

from .naive import naive_paste


def naive_paste_incremental(reader, output_path, delimeter='', batch_size=2, cell_preprocessor=None, temp_dir_path=None, keep_input_order=True):
    if batch_size < 1:
        return

    if batch_size == 1 or batch_size >= len(reader.paths):
        naive_paste(reader, output_path, delimeter, cell_preprocessor)
        return

    start = 0
    original_input_paths = reader.paths

    with tempfile.TemporaryDirectory(dir=temp_dir_path) as temp_dir:
        while True:
            end = start + batch_size
            batch = original_input_paths[start : end]
            if not batch:
                break

            temp_output_path = os.path.join(temp_dir, '%s_%s' % (start, end))

            reader.paths = batch
            naive_paste(reader, temp_output_path, delimeter, cell_preprocessor)

            start += batch_size
            if keep_input_order:
                original_input_paths.insert(start, temp_output_path)
            else:
                original_input_paths.append(temp_output_path)

        shutil.copyfile(temp_output_path, output_path)
