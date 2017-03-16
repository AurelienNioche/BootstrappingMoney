import numpy as np
import itertools as it
from timeit import timeit
#
#
# def f(a, b):
#
#     c = a.intersection(b)
#
#
# def g(c, d):
#
#     e = np.intersect1d(c, d)
#
#
# def init():
#     a = set(it.permutations(np.arange(100), r=2))
#     b = set(it.permutations(np.arange(50), r=2))
#
#     c = np.array(list(it.permutations(np.arange(100), r=2)), dtype=[('x', int, 1), ('y', int, 1)])
#     d = np.array(list(it.permutations(np.arange(50), r=2)), dtype=[('x', int, 1), ('y', int, 1)])
#
#     return a, b, c, d
#
#
# if __name__ == "__main__":
#
#     print(timeit("f(a, b)", setup="from __main__ import f, g, init; a, b, c, d = init()", number=10**4))
#     print(timeit("g(c, d)", setup="from __main__ import f, g, init; a, b, c, d = init()", number=10**4))


class A(object):

    def __init__(self):
        self.n_goods = 3
        self.generator_of_production_preferences = self.generate_production_pref()

    @staticmethod
    def generate_production_pref(self):
        all_possible_production_preferences = list(it.permutations(range(self.n_goods), r=self.n_goods))
        np.random.shuffle(all_possible_production_preferences)
        len_possibilities = len(all_possible_production_preferences)
        i = -1
        while True:
            i += 1
            yield all_possible_production_preferences[i % len_possibilities]

def main():

    a = A()
    for i in range(30):
        print(next(a.generate_production_pref))


if __name__ == "__main__":
    main()