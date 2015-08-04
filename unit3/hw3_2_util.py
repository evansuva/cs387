
def square(x):
    return x * x

def mod_exp(a, b, q):
    """return `a`**`b` (mod q)"""
    if b == 0:
        return 1
    if b % 2 == 0:
        return square(mod_exp(a, b/2, q)) % q
    else:
        return a * mod_exp(a, b-1, q) % q
    
