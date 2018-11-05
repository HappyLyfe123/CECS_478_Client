from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
import hashlib, hmac
import base64

AES_KEY_LENGTH = 32
IV_LENGTH = 16
RSA_KEY_LENGTH = 256
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

#User for decryting messages sent
def decrypt_message(received_message, private_key_path, password):
    
    #Get client RSA private key
    f = open(private_key_path, 'r')
    private_key = RSA.importKey(f.read(), passphrase= password)
    private_key = PKCS1_OAEP.new(private_key)
    
    #Get the encrypted message form json object
    aes_hmac_key = private_key.decrypt(base64.b64decode(received_message['rsa_ciphertext']))
    ciphertext_aes = base64.b64decode(received_message['aes_ciphertext'])
    send_hmac_tag = base64.b64decode(received_message['hmac_tag'])
    
    #Set initalize aes and hmac key
    aes_key = aes_hmac_key[:AES_KEY_LENGTH]
    hmac_key = aes_hmac_key[AES_KEY_LENGTH:]
    
    # create HMAC object
    hmac_object = hmac.new(hmac_key, ciphertext_aes, digestmod=hashlib.sha256)

    # create HMAC integrity tag
        
    
    #Check if the hmac is the same
    if hmac_object.digest() == send_hmac_tag:
        iv = ciphertext_aes[:IV_LENGTH]
        aes = AES.new(aes_key, AES.MODE_CBC, iv)
        return unpad(aes.decrypt(ciphertext_aes[IV_LENGTH:])).decode('utf-8')
    else:
        return "Error"
