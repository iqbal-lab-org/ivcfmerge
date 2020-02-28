from contextlib import ExitStack
from tempfile import NamedTemporaryFile

from . import ivcfmerge


def ivcfmerge_batch(input_paths, output_path, batch_size=None, temp_dir=None):
    batch_size = batch_size or 1000

    if batch_size < 2 or batch_size > len(input_paths):
        batch_size = len(input_paths)

    if batch_size == len(input_paths):
        batch = input_paths
    else:
        work_queue = list(reversed(input_paths))

        while True:
            batch = []
            while work_queue and len(batch) < batch_size:
                batch.append(work_queue.pop())

            if len(batch) < batch_size or not work_queue:
                break

            tmp_filename = NamedTemporaryFile(dir=temp_dir).name
            _ivcfmerge(batch, tmp_filename)
            work_queue.append(tmp_filename)

    _ivcfmerge(batch, output_path)


def _ivcfmerge(input_paths, output_path):
    with ExitStack() as stack, open(output_path, 'w+') as outfile:
        infiles = map(lambda p: stack.enter_context(open(p)), input_paths)
        ivcfmerge(infiles, outfile)
