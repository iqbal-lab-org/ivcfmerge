import shutil
from contextlib import ExitStack
from queue import Queue
from tempfile import NamedTemporaryFile

from . import ivcfmerge


def ivcfmerge_batch(input_paths, output_path, batch_size=1000):
    work_queue = Queue()
    [work_queue.put(item) for item in input_paths]

    last_tmp_filename = ''

    while True:
        batch = []
        while not work_queue.empty() and len(batch) < batch_size:
            batch.append(work_queue.get_nowait())

        if len(batch) == 1:
            break

        with ExitStack() as stack, open(NamedTemporaryFile().name, 'w+') as tmp_outfile:
            infiles = map(lambda p: stack.enter_context(open(p)), batch)
            ivcfmerge(infiles, tmp_outfile)

            work_queue.put(tmp_outfile.name)
            last_tmp_filename = tmp_outfile.name

    shutil.copyfile(last_tmp_filename, output_path)
