import encrypter
import decrypter

print('Encrypting: Attack at Dawn')

public_key_path = ''
private_key_path = ''

encrypted_message = encrypter.encrypt_message('Attack at Dawn', public_key_path)

aes = encrypted_message.__getattribute__('aes_ciphertext')

rsa = encrypted_message.__getattribute__('rsa_ciphertext')

hmac = encrypted_message.__getattribute__('hmac_tag')

print('aes ciphertext: ' + aes)
print('rsa ciphertext: ' + rsa)
print('hmac tag: ' + hmac)

decoded_message = decrypter.decrypt_message(encrypted_message, private_key_path)

print('Decoded Message: ' + decoded_message)

