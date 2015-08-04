# HW3-4 Version 1
# 
# Implement the Rabin Miller test for primality
#

from hw3_4_util import mod_exp
from random import randrange

def rabin_miller(n, target=128):
    """
    returns True if prob(`n` is prime) <= 2**(-`target`)
    """
    ###############
    ## Start your code here
    def calculate_t(n):
        n = n - 1
        t = 0
        while n % 2 == 0:
            n = n / 2
            t += 1
        return t
    if n % 2 == 0:
        return False
    t = calculate_t(n)
    s = (n - 1) / (2 ** t)
    n_tests = target / 2 # 2 ** ((-1/2) * n_test) = 2 ** (-target)
    tried = set()
    if n_tests > n:
        raise Exception("n is too small")
    for i in range(n_tests):
        while True:
            a = randrange(1, n)
            if a not in tried:
                break
        tried.add(a)
        # there are two tests in Rabin-Miller
        # here is the first one
        if mod_exp(a, s, n) == 1:
            continue
        # and here is the second
        found = False
        for j in range(0, t):
            if mod_exp(a, 2**j*s, n) == (n - 1):
                found = True
                break
        if not found:
            # we failed them both, lets leave
            return False
    # if we made it here, all the tests have passed
    return True
    ## End of your code
    ###############
