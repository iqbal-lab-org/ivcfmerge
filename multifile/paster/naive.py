import shutil

from multifile.reader.header_aware import HeaderAwareMultifileReader
from multifile.reader.plain import PlainMultifileReader


def naive_paste(reader, output_path, delimeter='', cell_preprocessor=None):
    """Naive implementation of Unix's 'paste' utility.
    
    Assumptions:
    - All files have the same number of lines.
    """

    if len(reader.paths) == 1:
        shutil.copyfile(reader.paths[0], output_path)
        return

    with reader:
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
