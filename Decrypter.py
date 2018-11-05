from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib, hmac
import base64

AES_KEY_LENGTH = 32
IV_LENGTH = 16
RSA_KEY_LENGTH = 256

def decrypt_message(received_message, private_key_path, password):
    
    #Get client RSA private key
    f = open(private_key_path, 'r')
    private_key = RSA.importKey(f.read(), passphrase= password)
    private_key = PKCS1_OAEP.new(private_key)
    
    #Get the encrypted message form json object
    aes_hmac_key = private_key.decrypt(base64.b64decode(received_message['rsa_ciphertext']))
    ciphertext_aes = base64.b64decode(received_message['aes_ciphertext'])
    send_hmac_tag = base64.b64decode(received_message['hmac_tag'])
    
    
    aes_key = aes_hmac_key[:AES_KEY_LENGTH]
    hmac_key = aes_hmac_key[AES_KEY_LENGTH:]
    
    # create HMAC object
    hmac_object = hmac.new(hmac_key, ciphertext_aes, digestmod=hashlib.sha256)

    # create HMAC integrity tag
        
    
    #Check if the hmac is the same
    if hmac_object.digest() == send_hmac_tag:
        aes = AES.new(aes_key, AES.MODE_CTR, counter=Counter.new(128))
        return aes.decrypt(ciphertext_aes).decode('utf-8')
    else:
        return "Error"
