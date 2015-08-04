import beast_client as bc

padding = '\x00'*15

# going to cheat here and just use the same token
# so that I don't have to worry about the XOR
# but that shouldn't be a problem

resp = bc._send()
target_length = len(resp["message"])

token = resp["token"]


found = []
l_padding = 15
block = 0
while len(found) < target_length:
    if l_padding < 0:
        block += 1
        l_padding = 15
    start = block * 16
    end = (block + 1) * 16
    padding = '\x00' * l_padding
    #just care about the first 16 bytes
    target = bc._send(padding, token)["message"][start:end]
    
    # now, take what we know, and search for the next
    padding += "".join(found)

    for i in range(256):
        test = padding + chr(i)
        if bc._send(test, token)["message"][start:end] == target:
            print "Found!", i, chr(i)
            found.append(chr(i))
            break
    l_padding -= 1
    
