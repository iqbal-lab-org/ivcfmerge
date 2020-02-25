from tempfile import NamedTemporaryFile

from hypothesis import given, strategies as st

from ivcfmerge.batch import ivcfmerge_batch


@given(batch_size=st.integers(min_value=2))
def test_merging_example_input(batch_size):
    input_paths = [
        'tests/data/input/1.vcf',
        'tests/data/input/2.vcf',
        'tests/data/input/3.vcf',
        'tests/data/input/4.vcf',
        'tests/data/input/5.vcf',
        'tests/data/input/6.vcf',
    ]

    with NamedTemporaryFile('w+') as outfile:
        ivcfmerge_batch(input_paths, outfile.name, batch_size)
        output = outfile.read()

        assert output.count('##') == 11
        assert output.count('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t') == 1
        assert output.count('site') == len(input_paths)
