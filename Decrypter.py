from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import json
import base64
import zlib


def decrypt_message(encrypt_message, key):
    #Set the aes object for decryption
    iv = encrypt_message[0:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypt_message = aes.decrypt(encrypt_message)

    return decrypt_message

def get_aes_key(rsa_cipher_text):
    private_key = RSA.importKey("private.pem", passphrase="AndrewV34")
    return private_key.decrypt(rsa_cipher_text)

def get_keys(path):
    loaded_json = json.load(path)
    rsa_cipher_text = loaded_json[0]
    encrypt_message = loaded_json[1]
    hmac = loaded_json[2]

    return rsa_cipher_text, encrypt_message, hmac
    

