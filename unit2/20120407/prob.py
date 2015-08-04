def fact(n):
    if n == 1:
        return 1
    return n * fact(n-1)

def nmk(n, k):
    if n == k:
        return n
    else:
        return n * nmk(n - 1, k)

import math

def pmatch(n, k):
    return 1.0 - math.exp((-k * (k - 1)) / (2.0 * n))
