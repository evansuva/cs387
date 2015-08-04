from Crypto.Cipher import AES

def encrypt(key, msg): 
   enc = AES.new(key, AES.MODE_ECB)
   return enc.encrypt(msg)

def decrypt(key, msg): 
   enc = AES.new(key, AES.MODE_ECB)
   return enc.decrypt(msg)

cipher = encrypt('secretabcdefghij', 'Hello!1234567890')
plaintext = decrypt('secretabcdefghij', cipher)
print plaintext

