import numpy as np
import timeit
from time import time


def create_diversity_quantity_mapping(n, k):

    a = - (k - 1) / (n - 1)
    b = (k * n - 1) / (n - 1)

    f = lambda x: a*x + b

    mapping = [0]

    for i in range(1, n + 1):

        mapping.append(int(f(i))**2)

    return mapping


if __name__ == "__main__":

    print(create_diversity_quantity_dic(n=3, k=4))
