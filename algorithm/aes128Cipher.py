from Crypto.Cipher import AES
import base64


class AES128Cipher:
    def __init__(self, key):
        self.key = key.encode('utf-8')
        # Initialization Vector
        self.iv = b'\x10\x00\x01\x00\x11\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x00'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        text = text.encode('utf-8')
        length = 16 - (len(text) % 16)
        text += bytes([length]) * length
        ciphertext = cipher.encrypt(text)
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = base64.b64decode(text)
        decrypted_text = cipher.decrypt(ciphertext)
        padding = decrypted_text[-1]
        return decrypted_text[:-padding].decode('utf-8')

def main():
    key = "1234567890123456"  # 自己的密鑰 : 16 位up
    c = AES128Cipher(key)
    encrypted_text = c.encrypt("This is a test message.")
    decrypted_text = c.decrypt(encrypted_text)
    print("Encrypted Text:", encrypted_text)
    print("Decrypted Text:", decrypted_text)

if __name__ == "__main__":
    main()