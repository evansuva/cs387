### Unit 2 Homework

from Crypto.Random import random
from bits import *

# Remember, this is NOT secure cryptology code
# This is for fun and education.  Do not use this
# to protect nuclear launch codes


def gen_random_seq(seed, n):
    seq = []
    state = seed
    for unused in range(n):
        extract = [state[i] for i in range(0, len(state), 2)]
        seq.append(bits_to_dec(extract))
        for i in range(387):
            bits_inc(state)
        bits_rotate(state, 7)
    return seq


# seed: [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]

def random_seq(n):
    state = generate_sequence(lambda n: random.choice([0, 1]), 64)
    print state
    seq = gen_random_seq(state, n)        
    return seq

BITS = ('0', '1')
ASCII_BITS = 8

def display_bits(b):
    """converts list of {0, 1}* to string"""
    return ''.join([BITS[e] for e in b])

def seq_to_bits(seq):
    return [0 if b == '0' else 1 for b in seq]

def pad_bits(bits, pad):
    """pads seq with leading 0s up to length pad"""
    assert len(bits) <= pad
    return [0] * (pad - len(bits)) + bits

def bits_rotate(b, n):
    leftb = b[0:n]
    for i in range(0, len(b) - n):
        b[i] = b[i + n]
    for i in range(n):
        b[len(b) - n + i] = leftb[i]
        

def convert_to_bits(n):
    """converts an integer `n` to bit array"""
    result = []
    if n == 0:
        return [0]
    while n > 0:
        result = [(n % 2)] + result
        n = n / 2
    return result

def string_to_bits(s):
    def chr_to_bit(c):
        return pad_bits(convert_to_bits(ord(c)), ASCII_BITS)
    return [b for group in 
            map(chr_to_bit, s)
            for b in group]

def bits_to_char(b):
    assert len(b) == ASCII_BITS
    value = 0
    for e in b:
        value = (value * 2) + e
    return chr(value)

def bits_to_dec(b):
    value = 0
    for e in b:
        value = (value * 2) + e
    return value

def list_to_string(p):
    return ''.join(p)

def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + ASCII_BITS]) 
                    for i in range(0, len(b), ASCII_BITS)])

def pad_bits_append(small, size):
    # as mentioned in lecture, simply padding with
    # zeros is not a robust way way of padding
    # as there is no way of knowing the actual length
    # of the file, but this is good enough
    # for the purpose of this exercise
    diff = max(0, size - len(small))
    return small + [0] * diff

############
# CBC uses a 'black box encoder' as discussed in the lecture
#
# AES is a very common example of this, which is available
# in the Crypto library
#
# For testing purposes, here is AES and some other, silly, encoders
# 
# These, or others might be used to grade your code
# so your implementation should be independent of the encoder used
def non_encoder(block, key):
    """A basic encoder that doesn't actually do anything"""
    return pad_bits_append(block, len(key))

def xor_encoder(block, key):
    block = pad_bits_append(block, len(key))
    cipher = [b ^ k for b, k in zip(block, key)]
    return cipher

def aes_encoder(block, key):
    block = pad_bits_append(block, len(key))
    # the pycrypto library expects the key and block in 8 bit ascii 
    # encoded strings so we have to convert from the bit string
    block = bits_to_string(block)
    key = bits_to_string(key)
    ecb = AES.new(key, AES.MODE_ECB)
    return string_to_bits(ecb.encrypt(block))
###### END of example encoders ########

# this is an example implementation of 
# the electronic cookbook cipher
# illustrating manipulating the plaintext,
# key, and init_vec 
def electronic_cookbook(plaintext, key, block_size, block_enc):
    """Return the ecb encoding of `plaintext"""
    cipher = []
    # break the plaintext into blocks
    # and encode each one
    for i in range(len(plaintext) / block_size + 1):
        start = i * block_size
        if start >= len(plaintext):
            break
        end = min(len(plaintext), (i+1) * block_size)
        block = plaintext[start:end]
        cipher.extend(block_enc(block, key))
    return cipher

def ctr_mode(plaintext, key, block_size, ctr, block_enc):
    """Return the ecb encoding of `plaintext"""
    cipher = []
    # break the plaintext into blocks
    # and encode each one
    for i in range(len(plaintext) / block_size + 1):
        start = i * block_size
        if start >= len(plaintext):
            break
        end = min(len(plaintext), (i+1) * block_size)
        block = plaintext[start:end]
        cblock = block_enc(ctr, key)
        cblock = xor_bits(cblock, block)
        cipher.extend(cblock)
        bits_inc(ctr)
    return cipher

def bad_hash(s, block_size, key):
    ctr = [0] * block_size
    cipher = ctr_mode(s, key, block_size, ctr, non_encoder)
    output = [0] * block_size
    # xor all blocks into hash output
    for i in range(len(cipher) / block_size + 1):
        block = cipher[block_size * i:block_size * (i + 1)]
        output = xor_bits(output, block)
    return output
    
def test():
    key = string_to_bits('4h8f.093mJo:*9#$')
    iv = string_to_bits('89JIlkj3$%0lkjdg')
    plaintext = string_to_bits("One if by land; two if by sea")

    cipher = ctr_mode(plaintext, key, 128, iv, aes_encoder)
    print bits_to_string(cipher)
    
a1 = [0] * 128 * 2
a2 = xor_bits(a1, [0]*127 + [1] + [0]*127 + [1])

s1 = bits_to_string(a1)
s2 = bits_to_string(a2)

def check_match(s1, s2):
    h1 = bad_hash(s1)
    h2 = bad_hash(s2)
    print "h1: " + display_bits(h1)
    print "h2: " + display_bits(h2)
    print display_bits(xor_bits(h1, h2))
    
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

length = 88    
# print generate_sequence(lambda n: 0, length)
#print display_bits(generate_sequence(lambda n: 0 if n % 3 == 0 else 1, length))
#print display_bits(string_to_bits("Anyone who considers arithmetical methods of producing random digits is, of course, in a state of sin.")[:length])
#print display_bits(generate_sequence(lambda n: random.choice([0, 1]), length))
#print display_bits(generate_fake_random(length))


