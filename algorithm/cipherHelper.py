from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii


class CipherHelper:
    def __init__(self):
        self.algm = "Bit Exchanging Method"

    def print_binary_format(self, number):
        binary = [0] * 25
        index = 0
        while number > 0:
            binary[index] = number % 2
            number = number // 2
            index += 1
        for i in range(index - 1, -1, -1):
            print(binary[i], end="")
        print()

    def cipher(self, secret_key, data):
        if secret_key is None or len(secret_key) != 8:
            raise ValueError("Invalid key length - 8 bytes key needed!")

        secret_key = secret_key.encode('utf-8')
        data = data.encode('utf-8')

        cipher = DES.new(secret_key, DES.MODE_ECB)
        padded_data = pad(data, DES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return binascii.hexlify(encrypted_data).decode('utf-8')

    def decipher(self, secret_key, data):
        if secret_key is None or len(secret_key) != 8:
            raise ValueError("Invalid key length - 8 bytes key needed!")

        secret_key = secret_key.encode('utf-8')
        data = binascii.unhexlify(data)

        cipher = DES.new(secret_key, DES.MODE_ECB)
        decrypted_data = cipher.decrypt(data)
        unpadded_data = unpad(decrypted_data, DES.block_size)
        return unpadded_data.decode('utf-8')

def main():
    try:
        cipher_helper = CipherHelper()
        secret_key = "01234567"
        data = "test"

        encrypted_data = cipher_helper.cipher(secret_key, data)
        print("Encrypted Data:", encrypted_data)

        decrypted_data = cipher_helper.decipher(secret_key, encrypted_data)
        print("Decrypted Data:", decrypted_data)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
