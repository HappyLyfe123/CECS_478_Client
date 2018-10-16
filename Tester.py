import encrypter
import Decrypter
from Crypto.PublicKey import RSA

private_key_string = open("private.pem","r")
private_key = RSA.importKey(private_key_string, passphrase="AnderV34")
print(private_key_string)
#encrypt_message = encrypter.encrypt_message()