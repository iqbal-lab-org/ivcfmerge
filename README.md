# VCF Join

This repo provides a utility to join the genotype data from a large number of VCF files from a common pipeline into one, without using too much memory or exceeding the OS' file limit. It assumes a few things from the input:
* All input VCF files have the same headers and fixed fields' information (i.e. this utility will ignore those info from all but the first file).
* The order of the data lines is the same for all input files (i.e. this utility will simply join the n<sup>th</sup> line of the 1<sup>st</sup> file with the n<sup>th</sup> line of the 2<sup>nd</sup> file, etc., without checking if the two lines' fixed fields match or not).

## 1. Usage:
```
python vcf/join.py <file_of_input_paths> <path_to_output>
```
Where:
* `file_of_input_paths` is a plain text file where each line is the path to one of the VCFs to be joined.
* `path_to_output` is where to write the joined VCF.

## 2. Benchmark (using `/usr/bin/time`):
* 8600+ input files, where each file has 980k+ positions and 1 sample (around 100 MB each file):
  * Total run time: 12 hours
  * Maximum memory occupied: 200 MB
* (To be updated)

## 3. Caveats

### 3.1 Memory

This utility still read a whole line for each input file, which means that if an input file has a large number of samples (hence each line is really long), then the amount of memory occupied will be large as well.

Even if the initial input files only has one sample each, but the number of files exceed the number of the OS' file limit, this could still happen.

The reason is that, in order to avoid the OS' limit, the joining process has to be split into several stages, where each stage produce an intermediate result, and the final stage join them together. Since the final stage's intermediate results would contain a large number of samples, the utility would occupy a large amount of memory, as explained above.

Work is being done to divide the input files so that the final stage has as many small files as possible, instead of a few big files.

### 3.2 Disk space

The utility makes use of as much disk space as the total amount used by the input files, so users should specify a directory with enough space via the `-t` or `--temp-dir` option. If not specified, the choice will be left to the Python's `tempfile` utility ([docs](https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp)).

## Testing:
* Install the package locally:
  ```
  pip install -e .
  ```
* Run the tests:
  ```
  pytest
  ```
