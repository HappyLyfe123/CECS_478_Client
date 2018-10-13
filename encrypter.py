# This program will take in a message and an RSA public key.
# The output of the module will be RSA ciphertext, AES ciphertext and HMAC tag based on the input

from Crypto.PublicKey import RSA
import random


def encrypt_message(message, public_key_path):

#RSA Encryption
    print("running")

    # generate RSA object
    public_key = RSA.generate(2048)

    #extract public key from file path
    public_key = importKey(open(public_key_path, 'r').read())

    # set RSA encryption protocol
    cipher = PKCS2_OAEP.new(public_key)

    #encrypt message using RSA key
    ciphertext_rsa = cipher.encrypt(message, 16)


#AES Encryption
    # iv generation referenced from https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/#4_Encrypting_with_AES
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])

