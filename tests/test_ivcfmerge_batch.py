from contextlib import ExitStack
from tempfile import NamedTemporaryFile, TemporaryFile

from hypothesis import given, strategies as st

from ivcfmerge import ivcfmerge_batch, ivcfmerge
from tests.conftest import _input_paths


@given(batch_size=st.integers(min_value=2))
def test_merging_example_input(batch_size, input_paths):
    with NamedTemporaryFile('w+') as outfile:
        ivcfmerge_batch(input_paths, outfile.name, batch_size)
        output = outfile.read()

        assert output.count('##') == 11
        assert output.count('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t') == 1
        assert output.count('site') == len(input_paths)


@given(batch_size=st.one_of(
    st.integers(max_value=1),
    st.integers(min_value=len(_input_paths()))
))
def test_out_of_bound_batch_sizes_yield_the_same_output_as_normal_ivcfmerge(batch_size, input_paths):
    with ExitStack() as stack:
        files = map(lambda fn: stack.enter_context(open(fn)), input_paths)
        with TemporaryFile('w+') as outfile:
            ivcfmerge(files, outfile)
            outfile.seek(0)
            expected = outfile.read()

    with NamedTemporaryFile('w+') as outfile:
        ivcfmerge_batch(input_paths, outfile.name, batch_size)
        output = outfile.read()

    assert output == expected


@given(batch_size=st.integers())
def test_single_input_yields_the_same_output_as_normal_ivcfmerge(batch_size):
    input_paths = ['tests/data/input/1.vcf']

    with ExitStack() as stack:
        files = map(lambda fn: stack.enter_context(open(fn)), input_paths)
        with TemporaryFile('w+') as outfile:
            ivcfmerge(files, outfile)
            outfile.seek(0)
            expected = outfile.read()

    with NamedTemporaryFile('w+') as outfile:
        ivcfmerge_batch(input_paths, outfile.name, batch_size)
        output = outfile.read()

    assert output == expected
