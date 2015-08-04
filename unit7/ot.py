from Crypto.PublicKey import RSA
from Crypto import Random

def setup_ot():
    prng = Random.new().read
    key = RSA.generate(1024, prng)
    r1 = Random.get_random_bytes(8)
    r2 = Random.get_random_bytes(8)
    publickey = key.publickey()
    return publickey, r1, r2

def select_one(key, r1, r2, select):
    nonce = Random.get_random_bytes(8)
    select = r1 if select else r2
    result = select + pow(nonce, key.e, key.n)
    return result

