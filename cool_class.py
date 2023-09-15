from abc import ABC, abstractmethod
from algorithm.aes128Cipher import AES128Cipher
from algorithm.cipherHelper import CipherHelper
from algorithm.division_Algorithm import DivisionAlgorithm
class My_Cipher_Worker_I(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def set_cipher(self, cipher):
        pass
    @abstractmethod
    def encrypt(self, message):
        pass
    @abstractmethod
    def decrypt(self, message):
        pass

class My_AES128_Worker(My_Cipher_Worker_I):
    def __init__(self, key):
        assert (len(key) != 16) or (len(key) != 24) or (len(key) != 32)
        self.key = key
        self.cipher = AES128Cipher(self.key)

    def set_cipher(self, cipher):
        self.cipher = cipher

    def encrypt(self, message):
        return self.cipher.encrypt(message)

    def decrypt(self, message):
        return self.cipher.decrypt(message)

class My_Normal_Cipher_Worker(My_Cipher_Worker_I):
    def __init__(self, key):
        assert len(key) % 8 == 0
        self.key = key
        self.cipher = CipherHelper()

    def set_cipher(self, cipher):
        self.cipher = cipher

    def encrypt(self, message):
        return self.cipher.cipher(self.key, message)

    def decrypt(self, message):
        return self.cipher.decipher(self.key, message)

class My_Division_Maker():
    def __init__(self, encryption_type: str, key: str, message: str, max_msg_len: int):
        self.encryption_type = encryption_type
        self.key = key
        self.cipher = self.set_cipher()
        self.division_algorithm = DivisionAlgorithm()
        self.division_algorithm.set_values(message, max_msg_len)
        self.vals = self.division_algorithm.get_process()
        self.encryptd_vals = [self.encrypt(val) for val in self.vals]
    def set_cipher(self):
        if str(self.encryption_type).lower == "aes_128".lower:
            return My_AES128_Worker(self.key)
        elif str(self.encryption_type).lower == "normal".lower:
            return My_Normal_Cipher_Worker(self.key)
        else:
            raise Exception("Invalid Encryption Type (current support: AES_128, Normal)")
    def encrypt(self, message):
        return self.cipher.encrypt(message)
    def decrypt(self, message):
        return self.cipher.decrypt(message)

    def show_all_params(self):
        # show all class member varialbes
        print("Encryption Type:", self.encryption_type)
        print("Key:", self.key)
        print("Cipher:", self.cipher)
        print("Division Algorithm:", self.division_algorithm)
        print("Vals:", self.vals)
        print("Encrypted Vals:", self.encryptd_vals)

def main1():
    aes = My_AES128_Worker("123456781234567812345678")
    print( aes.encrypt("Hello") )
    print(aes.decrypt(aes.encrypt("Hello")))

def main2():
    normal = My_Normal_Cipher_Worker("12345678")
    print(normal.encrypt("Hello"))
    print(normal.decrypt(normal.encrypt("Hello")))

def main():
    aa = My_Division_Maker("normal", "12345678", "Hello I fine thank you and you???", 5)
    aa.show_all_params()

if __name__ == "__main__":
    main()



