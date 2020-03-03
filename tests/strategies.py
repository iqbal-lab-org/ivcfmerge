from hypothesis.strategies import composite, integers, from_regex


@composite
def vcf_lines(draw):
    n_columns = draw(integers(min_value=8, max_value=11))
    return draw(from_regex('^([^\t]+\t){%d}' % n_columns))
