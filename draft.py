import numpy as np
import itertools as it
from timeit import timeit


def f(a, b):

    c = a.intersection(b)


def g(c, d):

    e = np.intersect1d(c, d)


def init():
    a = set(it.permutations(np.arange(100), r=2))
    b = set(it.permutations(np.arange(50), r=2))

    c = np.array(list(it.permutations(np.arange(100), r=2)), dtype=[('x', int, 1), ('y', int, 1)])
    d = np.array(list(it.permutations(np.arange(50), r=2)), dtype=[('x', int, 1), ('y', int, 1)])

    return a, b, c, d


if __name__ == "__main__":

    print(timeit("f(a, b)", setup="from __main__ import f, g, init; a, b, c, d = init()", number=10**4))
    print(timeit("g(c, d)", setup="from __main__ import f, g, init; a, b, c, d = init()", number=10**4))
