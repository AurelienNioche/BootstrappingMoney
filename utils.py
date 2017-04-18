import numpy as np
from timeit import timeit


def derangement(array_like, max_tries=10**6):

    """Generate a derangement of `a`

    A derangement is a permutation of the elements of `a` where no element keeps
    its place. This method will generate permutations until a good one is found.
    To avoid an infinite loop, will raise ValueError if more than `max_tries`
    permutations have been tried unsuccesfully.

    :param array_like:  array-like structure, of elements distinct enough to be deranged.
    """
    assert len(array_like) > 1

    a = np.array(array_like)  # O(1) if `a` is already an np.array
    b = a.copy()
    np.random.shuffle(a)
    np.random.shuffle(b)

    while any(a == b):
        max_tries -= 1
        if max_tries < 0:
            raise ValueError("Number of tries at derangement exceeded")
        np.random.shuffle(b)

    return zip(a, b)


def constrained_sum_sample(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(np.random.randint(1, total, size=n - 1))
    return np.random.permutation([a - b for a, b in zip(dividers + [total], [0] + dividers)])

if __name__ == "__main__":

    # print(list(derangement([1, 2, 3])))
    print(timeit("derangement(np.arange(1000))", setup="import numpy as np; from __main__ import derangement", number=10**4))
    print(timeit("derangement(np.arange(1000))", setup="import numpy as np; from cmodule.cutils import derangement", number=10**4))