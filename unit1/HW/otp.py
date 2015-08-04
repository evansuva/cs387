#
# cs387: Homework 1 - One-Time Pad Code
#

from Crypto.Random import random
from bits import *  # can't do import in IDE, but might want to distribute this

### Question 
def random_sequence(n):
    return map(lambda x: random.choice([0, 1]), range(n))

def otp(m, k):
    assert len(m) == len(k)
    return [(mm + kk) % 2 for mm, kk in zip(m, k)]

key = random_sequence(7)
msg = otp(string_to_bits('N'), key)
print display_bits(msg)
mask = seq_to_bits('0010111')
corrupted = otp(mask, msg)
print bits_to_string(otp(corrupted, key))

###
### monoalphabetic
###


alphabet = tuple('abcdefghijklmnopqurstuvwxyz')

def generate_key(alpha):
    copy = list(alpha)
    random.shuffle(copy)
    return tuple(copy)

def monoalphabetic_encrypt(key, msg):
    return list_to_string([alphabet[key.index(c)] 
                           for c in msg])

def monoalphabetic_decrypt(key, msg):
    return list_to_string([key[alphabet.index(c)] 
                           for c in msg])

### question 4
import math

def fact(n):
    res = 1
    for i in range(1, n + 1):
        res = res * i
    return res

print math.log(fact(26), 26)

### two-time pad

## m1 and m2 removed

m1 = string_to_bits("MSTR")
m2 = string_to_bits("MSFT")

k1 = random_sequence(len(m1))
c1 = otp(m1, k1)
k2 = otp(k1, otp(m1, m2))
assert otp(m2, k2) == c1

print "C1 = " + display_bits(c1)
print "K1 = " + display_bits(k1)
print "M1 = " + display_bits(m1)
print "K2 = " + display_bits(k2)
print "M2 = " + display_bits(m2)







