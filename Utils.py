from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def AES_Encrypt(data,key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    return cipher_text,iv

def AES_Decrypt(cipher,key,iv):
    decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = decrypt_cipher.decrypt(cipher)
    return plain_text

key = get_random_bytes(16)
data = b'This is some secret data.'
print(data)
enc_data,iv=AES_Encrypt(data,key)
print(enc_data)
dec_data = AES_Decrypt(enc_data,key,iv)
print("Decrypted data:", dec_data.decode())