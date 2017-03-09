import numpy as np
from time import time


def f(x):
    return x**2
n = 1000

operations = 100

t0 = time()
c = np.arange(n)[::-1]
for i in range(operations):
    c[:] = f(c)

print("numpy time:", time() - t0)

t0 = time()
c = list(range(n, 0, -1))

for i in range(operations):
    print(i)
    for j in range(len(c)):
        c[j] = f(c[j])

print("'list' time:", time() - t0)