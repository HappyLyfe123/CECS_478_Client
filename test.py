import encrypter
import decrypter

print('Encrypting: Attack at Dawn')


PUBLIC_KEY_PATH = './public.pem'
PRIVATE_KEY_PATH = './private.pem'
PASSWORD = 'Visal'

encrypted_message = encrypter.encrypt_message('Attack at Dawn', PUBLIC_KEY_PATH)

aes = encrypted_message['aes_ciphertext']
rsa = encrypted_message['rsa_ciphertext']
hmac = encrypted_message['hmac_tag']

decrypting_message = decrypter.decrypt_message(encrypted_message, PRIVATE_KEY_PATH, PASSWORD)

print('Decoded Message: ' + decrypting_message)

