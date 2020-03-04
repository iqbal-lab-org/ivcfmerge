# ivcfmerge: Incremental VCF merge

## 1. Purpose

We provides a utility to merge a large number of VCF files (possibly too many to open at once) incrementally, that only use almost as much memory as one merged line takes.

## 2 Important assumptions

* All input VCFs are positionally sorted, and the values for the FILTER column of each position are the same for all samples.
* All input VCFs have the same headers and the same number of positions.
* All input VCFs have the FORMAT column.

## 3. Output format

Since the FILTER value for each sample is different, we omit (set to `.`) the FILTER column in the merged result, and append the original FILTER value for each sample in their call data. Its format is described by the `FT` field in the `FORMAT` column.

For example: These two input lines:

NC_000962.3 11 . A C . **MIN_GCP** . GT:DP:COV:GT_CONF:GT_CONF_PERCENTILE 0/0:6:6,0:73.54:0.74

and

NC_000962.3 11 . A C . **MIN_DP;MIN_GCP** . GT:DP:COV:GT_CONF:GT_CONF_PERCENTILE 0/0:3:3,0:36.98:0.01

will produce this output line:

NC_000962.3 11 . A C . **.** . GT:DP:COV:GT_CONF:GT_CONF_PERCENTILE:**FT** 0/0:6:6,0:73.54:0.74:**MIN_GCP** 0/0:3:3,0:36.98:0.01:**MIN_DP;MIN_GCP**


## 4. Usage

You can use the utility as either:

* [A Python library](#python-usage)
* [A Python script](#cli-usage)

### <a name="python-usage">3.1 In Python</a>

#### 4.1.1 If the number of input files is small (can be opened all at once)

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

#### 4.1.2 If the number of input files is big (cannot be opened all at once)

```python
from ivcfmerge import ivcfmerge_batch

filenames = [...]    # List/iterator of relative/absolute paths to input files
output_path = '...'  # Where to write the merged VCF to
batch_size = 1000    # How many files to open and merge at once

ivcfmerge_batch(filenames, output_path, batch_size)
```

##### 4.1.2.1 You may also need to specify a temporary directory

That has at least as much space as that occupied by the input files to store intermediate results, in the batch processing version.

```python
...
temp_dir = '...'  # for example, a directory on a mounted disk like /mnt/big_disk/tmp or /media/big_disk/tmp

ivcfmerge_batch(filenames, output_path, batch_size, temp_dir)
```

### <a name="cli-usage">3.2 Command line interface</a>

#### 4.2.1 If the number of input files is small (can be opened all at once)

```shell script
# Prepare a file of paths to input VCF files
> cat input_paths.txt
1.vcf
2.vcf
...

> python ivcfmerge.py input_paths.txt path/to/output/file
```

#### 4.2.2 If the number of input files is big (cannot be opened all at once) 

```shell script
# Prepare a file of paths to input VCF files
> cat input_paths.txt
1.vcf
2.vcf
...

> python ivcfmerge_batch.py --batch-size 1000 input_paths.txt path/to/output/file
```

##### 4.2.2.1 You may also need to specify a temporary directory

That has at least as much space as that occupied by the input files to store intermediate results, in the batch processing version.

```shell script
...

> python ivcfmerge_batch.py --batch-size 1000 --temp-dir /path/to/tmp/dir input_paths.txt path/to/output/file
```

## 5. Important parameters
 
### 5.1 `batch_size`

Indicates how many files to open and merge each batch, for the batch processing version.

The default value for this parameter is 1000.

### 5.2 `temp_dir`

For the batch processing version, the utility needs to store the intermediate results somewhere with as much space as the total space occupied by the input files.

By default, the choice is left to the [tempfile](https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryFile) library. On Unix/Linux, this is usually `/tmp`.
