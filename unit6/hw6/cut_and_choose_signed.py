# Write the code for the cut-and-choose process
# of blind signatures

# First, Alice generates 100 bills for some
# amount.
# The bills are sent to the bank.  The bank
# picks one and signs it.
# Before sending it back to Alice, the bank
# asks for the random nonces for the other 99 bills
# The bank verifies the nonces and the amounts
# before sending back the signed bill

from Crypto.Util.number import GCD, inverse
from Crypto.Random import random
from unit6_util import string_to_bits, bits_to_int, pad_to_block, bits_to_string, convert_to_bits
import re

def create_bill(bill_number, bill_amount):
    return "Bill %d. IPBank %d" % (bill_number, bill_amount)

def bill_value(bill):
    print bill
    m = re.match("Bill \d*. IPBank (\d*)", bill)
    return int(m.group(1))

BANK_PUBLIC_KEY = (65537L, 146605267664968305757478488924026371034279663748432168896352333338344662802484320667649241137968415481826877512428632071426825921963704188324773006253432133951867548217268558652196457406282093300704326236710745110041671406733381071035768220531466030063347486543092022483351958440259179724216272703778522201967L)

#########
# Code for Alice
def random_nonce(bits=50):
    while True:
        test = random.getrandbits(50)
        if GCD(test, BANK_PUBLIC_KEY[1]) == 1:
            return test

def blind_msg(msg, nonce, e, n):
    return (msg * pow(nonce, e, n)) % n

_NONCES = None
def generate_bills(bill_amount, bill_count=100):
    global _NONCES
    _NONCES = []
    bills = []
    for _ in range(bill_count):
        bill = create_bill(random.randint(0, 100), bill_amount)
        bill_int = bits_to_int(string_to_bits(bill))
        nonce = random_nonce()
        t = blind_msg(bill_int, nonce, BANK_PUBLIC_KEY[0], BANK_PUBLIC_KEY[1])
        _NONCES.append(nonce)
        bills.append(t)
    return bills

def send_nonces(select_bill):
    return [n for i,n in enumerate(_NONCES) if i != select_bill]

##########
# Code for the bank
def sign_bill(bill):
    return pow(bill, _BANK_PRIVATE_KEY, BANK_PUBLIC_KEY[1])    

_BANK_PRIVATE_KEY = 40160586697425515254955388736943183837807998585159569833776545164156151964432320810325569161694111160798296107246764904989941647878517193234274528606250921861797675796157384299290208363046057168831417657336178672805630150267562009631690725301405637880870922628396388936009628239314530865889540780573312928073L
_ALL_BILLS = None # keep all of the bills
_SIGNED_BILL = (None, None) # keep the index and signature of the signed bill
def pick_and_sign_bill(bills):
    global _ALL_BILLS
    global _SIGNED_BILL
    choosen = random.randint(0, len(bills)-1)
    signature = sign_bill(bills[choosen])
    _SIGNED_BILL = (choosen, signature)
    _ALL_BILLS = [b for i,b in enumerate(bills) if i != choosen]
    return choosen # return the index of the choosen bill
    
def test_remove():
    m = 55
    r = 100
    msg = (m * pow(r, BANK_PUBLIC_KEY[0], BANK_PUBLIC_KEY[1])) % BANK_PUBLIC_KEY[1]
    new_m = remove_nonce(msg, r)
    assert m == new_m
    msg = blind_msg(m, r, BANK_PUBLIC_KEY[0], BANK_PUBLIC_KEY[1])
    new_m = remove_nonce(msg, r)
    assert m == new_m
    
def verify_bills_and_return_signed(nonces, value):
    if not _verify(_ALL_BILLS, nonces, value):
        return None
    return _SIGNED_BILL[1]

def message_value(message):
    message = bits_to_string(pad_to_block(convert_to_bits(message), 8))
    return bill_value(message) 

def remove_nonce(bill, nonce):
    big_nonce = pow(nonce, BANK_PUBLIC_KEY[0], BANK_PUBLIC_KEY[1])
    nonce_inverse = inverse(big_nonce, BANK_PUBLIC_KEY[1])
    assert big_nonce * nonce_inverse % BANK_PUBLIC_KEY[1] == 1
    message = (bill * nonce_inverse) % BANK_PUBLIC_KEY[1]
    return message

def _verify(bills, nonces, value):
    ###########
    ### Your code here
    for bill, nonce in zip(_ALL_BILLS, nonces):
        message = remove_nonce(bill, nonce)
        test_value = message_value(message)
        if test_value != value:
            return False

    return True
    ###########


def test():
    value = 50
    # Alice generates some bills
    bills = generate_bills(value)
    # and sends them to the bank.
    # The bank picks one and sends
    # back which one
    i = pick_and_sign_bill(bills)
    # Alice now needs to send back 
    # the random nonces
    nonces = send_nonces(i)
    # bank checks the nonces and
    # if they pass, returns the signed bill
    signed = verify_bills_and_return_signed(nonces, value)
    assert bills[i] == pow(signed, BANK_PUBLIC_KEY[0], BANK_PUBLIC_KEY[1])
