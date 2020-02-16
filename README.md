# Join the genotype data of multiple VCF files into one.

## Usage:
```
python vcf/join.py <file_of_input_paths> <path_to_output>
```
Where:
* `file_of_input_paths` is a plain text file where each line is the path to one of the VCFs to be joined.
* `path_to_output` is where to write the joined VCF.

## Benchmark (using `/usr/bin/time`):
* 95 input files, where each file has 980k+ positions and 1 sample (around 100MB each file):
  * Total run time: 2 minutes
  * Maximum memory occupied: 15MB
* (To be updated)

## Testing:
* Install the package locally:
  ```
  pip install -e .
  ```
* Run the tests:
  ```
  pytest
  ```
