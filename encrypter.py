# This program will take in a message and an RSA public key.
# The output of the module will be RSA ciphertext, AES ciphertext and HMAC tag based on the input

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256
import os
import hashlib, hmac
import json
import random
import base64


def encrypt_message(message, public_key_path):

#RSA Encryption

    #extract public key from file path
    public_key = RSA.importKey(open(public_key_path, 'r').read())

    # set RSA encryption protocol
    rsa_cipher = PKCS1_OAEP.new(public_key)


#AES Encryption

    # iv generation referenced from https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/#4_Encrypting_with_AES
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])

    aes_key = os.urandom(32)

    aes_ctr = Counter.new(128)

    aes_cipher = AES.new(aes_key, AES.MODE_CTR, counter=aes_ctr)


    # encrypt message
    ciphertext_aes = iv + aes_cipher.encrypt(message)

    # create HMAC key
    hmac_key = os.urandom(32)

    # create HMAC object
    hmac_object = hmac.new(hmac_key, ciphertext_aes, digestmod=hashlib.sha256)

    # create HMAC integrity tag
    hmac_tag = hmac_object.digest()

    # concatenate aes and hmac keys
    keys = aes_key + hmac_key

    # encrypt concatenated keys
    ciphertext_rsa = rsa_cipher.encrypt(keys)

    # create object holding values that will be returned
    output = {}
    output['rsa_ciphertext'] = base64.b64encode(ciphertext_rsa).decode('utf-8')
    output['aes_ciphertext'] = base64.b64encode(ciphertext_aes).decode('utf-8')
    output['hmac_tag'] = base64.b64encode(hmac_tag).decode('utf-8')

    output_file = 'encrypted_message.rsa'

    # write output to file using json
    out = open(output_file, 'w')
    out.write(json.dumps(output))
    out.close()

