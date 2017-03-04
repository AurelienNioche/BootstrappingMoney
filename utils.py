import numpy as np


def derangement(a, max_tries=100000):
    """Generate a derangement of `a`

    A derangement is a permutation of the elements of `a` where no element keeps
    its place. This method will generate permutations until a good one is found.
    To avoid an infinite loop, will raise ValueError if more than `max_tries`
    permutations have been tried unsuccesfully.

    :param a:  array-like structure, of elements distinct enough to be deranged.
    """
    a = np.array(a) # O(1) if `a` is already an np.array
    b = a.copy()
    np.random.shuffle(b)

    while any(a == b):
        max_tries -= 1
        if max_tries < 0:
            raise ValueError("Number of tries at derangement exceeded")
        np.random.shuffle(b)

    return zip(a, b)
