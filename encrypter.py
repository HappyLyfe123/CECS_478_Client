# This program will take in a message and an RSA public key.
# The output of the module will be RSA ciphertext, AES ciphertext and HMAC tag based on the input

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import os
import hashlib, hmac
import json
import base64

IV_LENGTH = 16
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def encrypt_message(message, public_key_path):

#RSA Encryption

    #extract public key from file path
    public_key = RSA.importKey(open(public_key_path, 'r').read())

    # set RSA encryption protocol
    rsa_cipher = PKCS1_OAEP.new(public_key)


#AES Encryption

    #Pad the message
    message = pad(message)

    # random iv generation
    iv = os.urandom(AES.block_size)

    aes_key = os.urandom(32)

    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)


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
    
    return json.loads(json.dumps(output))
