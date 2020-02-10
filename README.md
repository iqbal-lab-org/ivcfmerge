# Run without install

```
python3 scripts/no_install/paste_vcf.py -h
```

# Install

```
pip3 install .
```

## Commands available after install

```
paste_vcf -h
```

# List of modules

* `multifile/paster/vcf/paster.py`: VCF paster entry point
* `multifile/paster/incremental.py`: Generic incremental paster which the VCF paster is based on
* `multifile/paster/naive.py`: Generic paster which the incremental paster is based on
* `multifile/reader/header_aware.py`: Header-aware incremental reader which the generic paster uses to read "combined line" from multiple files
* `multifile/reader/base.py`: Base incremental reader which the header-aware one is based on

# Development

## Dev dependencies

```
pip3 install -r requirements/dev.txt
```

## (Optional) Install editable version

```
pip3 install -e .
```

## Run all tests

```
pytest
```