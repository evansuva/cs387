###
### Some routines for manipulating bits
###
###

import itertools
import binascii
from Crypto.Random import random

BITS = ('0', '1')
HEX_DIGITS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')

def display_bits(b): # converts list of {0, 1}* to string
    return ''.join([BITS[e] for e in b])

def display_hex(b):
    return ''.join([BITS[e] for e in b])

def pad_bits(seq, pad): # pads seq with leading 0s up to length pad
    assert len(seq) <= pad
    return [0] * (pad - len(seq)) + seq
        
def dec_to_bits(n): # integer to binary
    result = []
    while n > 0:
        result = [(n % 2)] + result
        n = n / 2
    return result

def xor_bits(b1, b2):
    return [(bb1 + bb2) % 2 for bb1, bb2 in zip(b1, b2)]
    
def bits_inc(b):
    carry = 0
    for i in range(len(b) - 1, -1, -1):
        if b[i] == 0:
            b[i] = 1
            return
        else:
            b[i] = 0
    
def bits_to_dec(n):
    result = 0
    for b in n:
        result = result * 2 + b
    return result

def string_to_bits(s):
    return [b for group in map(lambda c: pad_bits(dec_to_bits(ord(c)), 8), s) \
              for b in group ]

def bits_to_char(b):
    assert len(b) == 8
    value = 0
    for e in b:
        value = (value * 2) + e
    return chr(value)

def bits_to_hex(b):
    assert len(b) == 4
    return HEX_DIGITS[bits_to_dec(b)]
    
def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + 8]) for i in range(0, len(b), 8)])

def bits_to_hexstring(b):
    return ''.join([bits_to_hex(b[i:i + 4]) for i in range(0, len(b), 4)])

def string_to_hexstring(s):
    return bits_to_hexstring(string_to_bits(s))

def hexstring_to_string(s):
    return bits_to_string(hexstring_to_bits(s))

def hex_to_bits(h):
    value = HEX_DIGITS.index(h)
    assert value != -1
    res = pad_bits(dec_to_bits(value), 4)
    assert (bits_to_hex(res) == h)
    return res

def bin_to_hexstring(b):
    return binascii.b2a_hex(b)

def bin_to_string(b):
    return hexstring_to_string(binascii.b2a_hex(b))

def string_to_bin(s):
    return binascii.a2b_hex(string_to_hexstring(s))

def is_hexstring(s):
    return len(s) % 2 == 0 and all([c in HEX_DIGITS for c in s])
    
def hexstring_to_bits(b):
    res = []
    for h in b:
        res += hex_to_bits(h)
    return res
        
def generate_sequence(f, n):
    return map(f, range(n))

def random_sequence(n):
    return generate_sequence(lambda n: random.choice([0, 1]), n)

    
