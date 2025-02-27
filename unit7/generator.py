def mod_exp(a, b, q):
    if b == 0:
        return 1
    if b % 2 == 0:
        x = mod_exp(a, b / 2, q)
        return (x * x) % q
    else:
        return (a * mod_exp(a, b - 1, q)) % q

def is_primitive_root(g, q):
    reached = []
    x = g
    while True:
        if x in reached:
            break
        reached.append(x)
        x = (x * g) % q
    return len(reached) == q - 1

def primitive_roots(q):
    """Brute force search for primitive roots of a prime q."""
    return [i for i in range(1, q) if is_primitive_root(i, q)]

def generator_permutation(g, q):
    return [mod_exp(g, i, q) for i in range(1, q)]

def simulate_dh(g, q):
    x_a = 3
    x_b = 5
    y_a = pow(g, x_a, q)
    y_b = pow(g, x_b, q)
    k_ab = pow(y_b, x_a, q)
    k_ba = pow(y_a, x_b, q)
    print k_ab, k_ba
    assert k_ab == k_ba









