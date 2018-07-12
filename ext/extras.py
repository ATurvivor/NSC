from operator import mul
from functools import reduce


def prod(iterable):
    return reduce(mul, iterable, 1)
