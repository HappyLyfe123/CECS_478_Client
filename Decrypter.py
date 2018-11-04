from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import json
import base64
import zlib


AESKEYLENGTH = 16
IVLENGTH = 16
RSAKEYLENGTH = 256

def decrypt_message(encrypt_message, aes_private_key_path):
    
    #Get client RSA private key
    private_key = RSA.importKey(open(aes_private_key_path,'r').read())
    
    #Get the encrypted message json object
    loaded_json = json.load(encrypt_message)
    rsa_cipher_text = loaded_json[0]
    hmac_key = rsa_cipher_text[RSAKEYLENGTH: ]
    encrypt_message = loaded_json[1]
    sent_hmac = loaded_json[2]
    
    #Calculate hamc
    curr_hmac = hmac.new(hmac_key, encrypt_message, digestmod=hashlib.sha256)
    
    private_key.decrypt(rsa_cipher_text)
    
    #Check if the hmac is the same
    if curr_hmac == sent_hmac:
        encrypt_message = base64.b64decode(encrypt_message)
        iv = encrypt_message[:IVLENGTH]
        aes = AES.new(key, AES.MODE_CTR, iv)
        decrypt_message = aes.decrypt(encrypt_message[IVLENGTH:])
        out = (open_file, 'w')
        out.write(decrypt_message)
        out.close()
        return true
    else:
        return false
