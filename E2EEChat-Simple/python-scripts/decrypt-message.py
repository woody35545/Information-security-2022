from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import base64

def decode_base64(b64):
    return base64.b64decode(b64)

def read_from_base64():
    return [ decode_base64(input()), decode_base64(input()), decode_base64(input())]

def decrypt_message(key, iv, message):
    # AES 256 복호화 구현
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg_decrypted = cipher.decrypt(message)
    msg_decrypted = unpad(msg_decrypted, AES.block_size)
    return msg_decrypted

[secretkey, iv, message] = read_from_base64()

result = decrypt_message(secretkey, iv, message).decode('utf-8')
print(result)