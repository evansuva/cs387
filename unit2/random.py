### Randomness!

from Crypto.Random import random
from bits import *

def generate_sequence(f, n):
    return map(f, range(n))

def alternate(x):
    if x % 3 == 0:
        return 0
    else:
        return 1

def string_selector(s):
    return lambda n: ord(s[n % len(s)]) % 2

def generate_fake_random(n):
    ## generates a trick random sequence - avoids runs > 3
    repetition = 0
    previous = None
    res = []
    for i in range(n):
        x = random.choice([0, 1])
        if x == previous:
            repetition += 1
            if repetition > 2:
                x = (x + 1) % 2
                repetition = 1
                previous = x
        else:
            previous = x
            repetition = 1
        res.append(x)
    return res
    
def random_sequence(n):
    return generate_sequence(lambda n: random.choice([0, 1]), n)


def find_random(b):
    i = 0
    while True:
        i = i + 1
        seq = random_sequence(b)
        if sum(seq) == 0:
            return i

def average_find_random(b, n):
    total = 0.0
    for unused in range(n):
        total += find_random(b)
    return total / n

    

length = 88    
# print generate_sequence(lambda n: 0, length)
#print display_bits(generate_sequence(lambda n: 0 if n % 3 == 0 else 1, length))
#print display_bits(string_to_bits("Anyone who considers arithmetical methods of producing random digits is, of course, in a state of sin.")[:length])
#print display_bits(generate_sequence(lambda n: random.choice([0, 1]), length))
#print display_bits(generate_fake_random(length))


