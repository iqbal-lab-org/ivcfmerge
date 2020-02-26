from contextlib import ExitStack
from queue import Queue
from tempfile import NamedTemporaryFile

from . import ivcfmerge


def ivcfmerge_batch(input_paths, output_path, batch_size=1000):
    if batch_size < 2 or batch_size > len(input_paths):
        batch_size = len(input_paths)

    if batch_size == len(input_paths):
        batch = input_paths
    else:
        work_queue = Queue()
        [work_queue.put(item) for item in input_paths]

        while True:
            batch = []
            while not work_queue.empty() and len(batch) < batch_size:
                batch.append(work_queue.get_nowait())

            if len(batch) < batch_size or work_queue.empty():
                break

            tmp_filename = NamedTemporaryFile().name
            _ivcfmerge(batch, tmp_filename)
            work_queue.put(tmp_filename)

    _ivcfmerge(batch, output_path)


def _ivcfmerge(input_paths, output_path):
    with ExitStack() as stack, open(output_path, 'w+') as outfile:
        infiles = map(lambda p: stack.enter_context(open(p)), input_paths)
        ivcfmerge(infiles, outfile)
