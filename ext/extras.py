from operator import mul

def prod(iterable):
    return reduce(mul, iterable, 1)


