import numpy as np


def derangement(a, max_tries=10**6):
    """Generate a derangement of `a`

    A derangement is a permutation of the elements of `a` where no element keeps
    its place. This method will generate permutations until a good one is found.
    To avoid an infinite loop, will raise ValueError if more than `max_tries`
    permutations have been tried unsuccesfully.

    :param a:  array-like structure, of elements distinct enough to be deranged.
    """
    assert len(a) > 1

    a = np.array(a)  # O(1) if `a` is already an np.array
    b = a.copy()
    np.random.shuffle(a)
    np.random.shuffle(b)

    while any(a == b):
        max_tries -= 1
        if max_tries < 0:
            raise ValueError("Number of tries at derangement exceeded")
        np.random.shuffle(b)

    return zip(a, b)

# def derangement(array_like):
#
#     assert len(array_like) > 1
#
#     a = list(array_like)
#     b = list(array_like)
#
#     while True:
#         error = 0
#         a = np.random.permutation(a)
#         b = np.random.permutation(b)
#         for i, j in zip(a, b):
#             if i == j:
#                 error = 1
#                 break
#         if not error:
#             break
#
#     return zip(a, b)

if __name__ == "__main__":

    print(list(derangement([1, 2, 3])))