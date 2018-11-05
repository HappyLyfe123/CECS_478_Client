import encrypter
import decrypter

print('Encrypting: Attack at Dawn')

public_key_path = '/home/jake/Documents/CECS 478/Project Code/phase 3/venv/keys/public.pem'
private_key_path = ''

encrypted_message = encrypter.encrypt_message('Attack at Dawn', public_key_path)

print(encrypted_message.keys())

aes = encrypted_message['aes_ciphertext']
rsa = encrypted_message['rsa_ciphertext']
hmac = encrypted_message['hmac_tag']

#decoded_message = decrypter.decrypt_message(encrypted_message, private_key_path)

#print('Decoded Message: ' + decoded_message)

