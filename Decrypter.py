from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import json
import base64
import zlib

private_key = RSA.importKey(open('private.pem','r').read())
print(private_key)


def decrypt_message(encrypt_message, key):
    #Set the aes object for decryption
    encrypt_message = base64.b64decode(encrypt_message)
    iv = encrypt_message[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypt_message = aes.decrypt(encrypt_message[16:])

    return decrypt_message

def get_aes_key(rsa_cipher_text):
    private_key = RSA.importKey(open('private.pem','r').read())
    return private_key.decrypt(rsa_cipher_text)

def get_data_json(path):
    loaded_json = json.load(path)
    rsa_cipher_text = loaded_json[0]
    encrypt_message = loaded_json[1]
    hmac = loaded_json[2]

    return rsa_cipher_text, encrypt_message, hmac
    

