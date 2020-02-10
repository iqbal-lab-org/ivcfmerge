import copy
from concurrent import futures
import math
import os
from multiprocessing import Queue
from queue import Empty
import shutil
import tempfile

from .naive import naive_paste


def naive_paste_incremental(reader, output_path, delimeter='', batch_size=2, cell_preprocessor=None, temp_dir_path=None, keep_input_order=True, max_workers=1):
    if batch_size < 1:
        return

    if batch_size == 1 or batch_size >= len(reader.paths):
        naive_paste(reader, output_path, delimeter, cell_preprocessor)
        return

    if keep_input_order:
        naive_paste_incremental_synchronous(reader, output_path, delimeter, batch_size, cell_preprocessor, temp_dir_path)
        return

    remaining_batches, last_batch_size = total_number_of_batches_and_last_batch_size(len(reader.paths), batch_size)

    work_queue = Queue()
    [work_queue.put_nowait(p) for p in reader.paths]

    with futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        with tempfile.TemporaryDirectory(dir=temp_dir_path) as temp_dir:
            while True:
                batch, remaining_batches = get_batch(work_queue, batch_size, remaining_batches, last_batch_size)
 
                cloned_reader = copy.deepcopy(reader)
                cloned_reader.paths = batch

                if remaining_batches == 0:
                    naive_paste(cloned_reader, output_path, delimeter, cell_preprocessor)
                    break

                future = executor.submit(process_one_batch, cloned_reader, delimeter, temp_dir, cell_preprocessor)
                future.add_done_callback(lambda ft: work_queue.put_nowait(ft.result()))


def process_one_batch(cloned_reader, delimeter, temp_dir, cell_preprocessor):
    start = os.path.basename(cloned_reader.paths[0])
    end = os.path.basename(cloned_reader.paths[-1])
    temp_output_path = os.path.join(temp_dir, '%s_%s' % (start, end))

    naive_paste(cloned_reader, temp_output_path, delimeter, cell_preprocessor)

    return temp_output_path


def total_number_of_batches_and_last_batch_size(input_size, batch_size):
    if input_size <= batch_size:
        n_batches = 1
        last_batch_size = input_size
        return n_batches, last_batch_size

    n_batches, remain = divmod(input_size, batch_size)
    n_results = n_batches  # just for clarity

    next_input_size = n_results + remain
    n_next_batches, last_batch_size = total_number_of_batches_and_last_batch_size(next_input_size, batch_size)

    total_n_batches = n_batches + n_next_batches

    return total_n_batches, last_batch_size


def get_batch(queue, batch_size, remaining_batches, last_batch_size):
    batch = []

    while (len(batch) < batch_size and remaining_batches > 1) or len(batch) < last_batch_size:
        try:
            batch.append(queue.get_nowait())
        except Empty:
            pass

    remaining_batches -= 1

    return batch, remaining_batches


def naive_paste_incremental_synchronous(reader, output_path, delimeter, batch_size, cell_preprocessor, temp_dir_path):
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
            original_input_paths.insert(start, temp_output_path)

        shutil.copyfile(temp_output_path, output_path)
