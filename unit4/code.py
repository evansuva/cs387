###
### Unit 4 Code
###

def euclid(a, b):
    if b == 0:
        return a
    return euclid(b, a % b)

def extended_euclid(a, b):
    """Returns (s, t) where as + bt = gcd(a, b)"""
    if b == 0:
        return (1, 0)
    else:
        (s, t) = extended_euclid(b, a % b)
        return (t, s - (a / b) * t)

### This is all ridiculously inefficient code for clarity, not for any
### practical purpose!

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def totient(n):
    """Brute force computation of Euler's totient (not for large n)."""
    return [i for i in range(n) if gcd(i, n) == 1]

def is_primitive_root(g, q):
    reached = []
    x = g
    while True:
        if x in reached:
            break
        reached.append(x)
        x = (x * g) % q
    return len(reached) == q - 1

def square(x): return x * x

def mod_exp(a, b, q):
    if b == 0:
        return 1
    if b % 2 == 0:
        return square(mod_exp(a, b / 2, q)) % q
    else:
        return (a * mod_exp(a, b - 1, q)) % q
    
def generator_permutation(g, q):
    return [mod_exp(g, i, q) for i in range(1, q)]

    
def primitive_roots(q):
    """Brute force search for primitive roots of a prime q."""
    return [i for i in range(1, q) if is_primitive_root(i, q)]

#def toy_diffie_helman(q, alpha):
    
