from multiprocessing import Pool
import copy

from multifile.paster.incremental import naive_paste_incremental


def naive_paste_parallel(reader, output_path, delimeter='', batch_size=2, cell_preprocessor=None, temp_dir_path=None, keep_input_order=True, n_processes=1, _recurred_run_count_auto=0):
    if n_processes <= 1:
        naive_paste_incremental(reader, output_path, delimeter, batch_size, cell_preprocessor, temp_dir_path, keep_input_order)
        return

    chunk_size = int(len(reader.paths) / n_processes)
    if chunk_size <= 2:
        naive_paste_incremental(reader, output_path, delimeter, batch_size, cell_preprocessor, temp_dir_path, keep_input_order)
        return

    readers = []
    output_paths = []
    start = 0
    while True:
        end = start + chunk_size

        chunk = reader.paths[start:end]
        if not chunk:
            break

        cloned_reader = copy.deepcopy(reader)
        cloned_reader.paths = reader.paths[start:end]

        readers.append(cloned_reader)
        output_paths.append(output_path + str(start) + str(_recurred_run_count_auto))

        start = end

    with Pool(n_processes) as p:
        args = []
        for i in range(len(readers)):
            args.append((readers[i], output_paths[i], delimeter, batch_size, cell_preprocessor, temp_dir_path, keep_input_order))

        p.starmap(naive_paste_incremental, args, 1)

    reader.paths = output_paths
    naive_paste_parallel(reader, output_path, delimeter, batch_size, cell_preprocessor, temp_dir_path, keep_input_order, n_processes, _recurred_run_count_auto + 1)
