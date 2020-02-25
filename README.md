# ivcfmerge: Incremental VCF merge

## Purpose

We provides a utility to merge a large number of VCF files (too many to open at once) incrementally, that only use as
much memory as each line in one of the input files takes (so the fewer samples you have in each of the input files, the
less memory you need).

## Usage

### In Python

```python
from contextlib import ExitStack
from ivcfmerge import ivcfmerge

filenames = [...]    # List/iterator of relative/absolute paths to input files
output_path = '...'  # Where to write the merged VCF to

with ExitStack() as stack:
    files = map(lambda fname: stack.enter_context(open(fname)), filenames)
    with open(output_path) as outfile:
        ivcfmerge(files, outfile)
```

## Batch size

An important parameter for this utility is `batch_size`, which indicates how many files to open and merge each batch,
since the total number of input files can exceed the number of open files allowed by the OS.

The default value for this parameter is 1000.
