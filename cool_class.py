from abc import ABC, abstractmethod
from algorithm.aes128Cipher import AES128Cipher
from algorithm.cipherHelper import CipherHelper
from algorithm.division_Algorithm import DivisionAlgorithm
import qrcode
from pathlib import Path
import os
import shutil
from glob import glob
import cv2
import numpy as np
from pyzbar.pyzbar import decode


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
        print("message:", message)
        #
        self.encryption_type = encryption_type
        self.key = key
        self.cipher = self.set_cipher()
        self.division_algorithm = DivisionAlgorithm()
        self.division_algorithm.set_values(message, max_msg_len)
        # raw data 分批
        self.vals = self.division_algorithm.get_process()
        # 每批分別加密，並且加上編號
        self.encryptd_vals = ["{0}-{1}".format((idx+1), self.encrypt(val)) for idx, val in enumerate(self.vals)]
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
        #print("Cipher:", self.cipher)
        #print("Division Algorithm:", self.division_algorithm)
        print("Vals:", self.vals)
        print("Encrypted Vals:", self.encryptd_vals)

def ensure_folder(folder_path, remake=False):
    """
    確保某個資料夾必定存在，因為會重新建立。

    @param folder_path:
        要建立的資料夾名。

    @param remake: (Default False)
        如果為 True，會刪除舊的目錄再重新建立。
    """
    if os.path.isdir(folder_path):
        if not remake:
            return
        else:
            shutil.rmtree(folder_path)
            os.makedirs(folder_path, 0o755)
    else:
        os.makedirs(folder_path, 0o755)




def main1():
    aes = My_AES128_Worker("123456781234567812345678")
    print( aes.encrypt("Hello") )
    print(aes.decrypt(aes.encrypt("Hello")))

def main2():
    normal = My_Normal_Cipher_Worker("12345678")
    print(normal.encrypt("Hello"))
    print(normal.decrypt(normal.encrypt("Hello")))

def main():
    aa = My_Division_Maker("normal", "12345678", "Hello how are you, I fine thank you and you?", 7)
    aa.show_all_params()
    return aa
def gogomakerQR(aa: My_Division_Maker):
    # 存檔根目錄
    output_path = Path("./output/qrcode")
    # 專屬子目錄名稱
    new_folder = "haha"
    # 確保、刷新目錄狀態
    ensure_folder(output_path.joinpath(new_folder), remake=True)

    # make some qr code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    for idx, msg in enumerate(aa.encryptd_vals):
        # build qr
        qr.add_data(msg)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # save qr
        img.save(output_path.joinpath(new_folder).joinpath("{0}-test.png".format(idx)))
        # refresh qr content
        qr.clear()

def detected_folder(folder):
    #detect qrcodr from image
    merge = ""
    selected_raw_msg = []
    for img in glob("{}/*.*".format(folder)):
        image = cv2.imread(img)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(image)
        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            selected_raw_msg.append(data)
    # process raw msg, sort it.
    # selected_raw_msg = ["1-c9f154450b9b95e4", "100-854848484848484", "4-f8e0b14e7fee80f4", "5-d24017e7f2be65f2",
    #            "3-503a3220602c52d0", "6-a36dbbf8894624a7", "7-dc3be62572e274b8", "2-975ff2f03953aae3"]

    # 將 list 的元素分割成 整數-編碼 部分，並將它們放入在新的 tuple list 中
    split_list = [(int(item.split('-')[0]), item) for item in selected_raw_msg]
    # 根據 tuple 的整数部分排序
    sorted_list = sorted(split_list, key=lambda x: x[0])
    # 從排序後的元组列表中提取原始元素
    result_list = [item[1] for item in sorted_list]
    # 印出 list, but 移除 '-'號

    ciphers = []
    for item in result_list:
        ciphers.append(item.split('-')[1])

    return ciphers


if __name__ == "__main__":
    aa = main()  # 製造訊息 -> 加密訊息 -> 分離訊息 -> 製造各分離訊息之 QRcode
    print()
    #  根據密文製造 qr code
    gogomakerQR(aa)
    print()
    # 從檔案讀取 qr code 並解碼
    ciphers_list = detected_folder("./output/qrcode/haha")
    print("crypted cipher:", ciphers_list)
    for cipher in ciphers_list:
        print(aa.cipher.decrypt(cipher), end='')


