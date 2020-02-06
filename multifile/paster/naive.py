import shutil

from multifile.reader.default import DefaultMultifileReader


def naive_paste(input_paths, output_path, delimeter='', from_line=0, n_header_lines=0, cell_preprocessor=None):
    """Naive implementation of Unix's 'paste' utility.
    
    Assumptions:
    - All files have the same number of lines.
    """

    if len(input_paths) == 1:
        shutil.copyfile(input_paths[0], output_path)
        return

    with DefaultMultifileReader(input_paths, from_line=from_line, n_header_lines=n_header_lines) as reader:
        output_file = open(output_path, 'w')

        for cell, metadata in reader:
            if metadata.get('skipped', False):
                continue

            if cell_preprocessor:
                cell = cell_preprocessor(cell, metadata)
            
            output_file.write(cell)

            if not cell.endswith('\n'):
                output_file.write(delimeter)

        output_file.close()
