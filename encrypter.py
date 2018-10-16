# This program will take in a message and an RSA public key.
# The output of the module will be RSA ciphertext, AES ciphertext and HMAC tag based on the input

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import os
import hmac, hashlib


def encrypt_message(message, public_key_path):

#RSA Encryption

    #extract public key from file path
    public_key = RSA.importKey(open(public_key_path, 'r').read())

    # set RSA encryption protocol
    rsa_cipher = PKCS2_OAEP.new(public_key)


#AES Encryption
    # iv generation referenced from https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/#4_Encrypting_with_AES
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])

    aes_key = os.urandom(32)

    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    # encrypt message
    ciphertext_aes = iv + aes_cipher.encrypt(message)

    # create HMAC tag
    hmac_key = os.urandom(32)

    hmac_object = hmac.new(hmac_key, ciphertext_aes, digestmod=hashlib.sha256)

    # concatenate aes and hmac keys
    keys = aes_key + hmac_key


