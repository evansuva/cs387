def display_bits(b):
    result = ''
    for e in b:
        assert b == 0 or b == 1
        result = result + str(e)
    return result




            
def convert_to_bits(n, pad): 
    result = []
    while n > 0:
        if n % 2 == 0:
            result = [0] + result
        else:
            result = [1] + result
        n = n / 2
    while len(result) < pad:
        result = [0] + result
    return result








def string_to_bits(s):
    result = []
    for c in s:
        result = convert_to_bits(ord(c), 7) + result
    return result





def bits_to_char(b):
    assert len(b) == 7
    value = 0
    for e in b:
        value = (value * 2) + e
    return chr(value)





    
def bits_to_string(b):
    result = ""
    for i in range(0, len(b), 7):
        result = bits_to_char(b[i:i+7]) + result
    return result



