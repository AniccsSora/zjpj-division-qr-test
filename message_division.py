import os
import random
from algorithm.aes128Cipher import AES128Cipher
from algorithm.cipherHelper import CipherHelper
from algorithm.division_Algorithm import DivisionAlgorithm
import qrcode as QRCode

class Message:
    def process_request(self, text):
        try:
            # 在這裡，您可以註解掉實際的 DB 讀取部分，並假設資料已經被寫入 DB
            # connection = DB().fun()
            # cursor = connection.cursor()
            # cursor.execute("TRUNCATE TABLE msg")
            # connection.commit()

            name = "Sample Name"  # 替換為實際的名稱
            id = "SampleID"  # 替換為實際的ID

            aes = AES128Cipher()
            cipher_helper = CipherHelper()

            division_algorithm = DivisionAlgorithm()
            division_algorithm.set_values(text, 9)
            val = division_algorithm.get_process()

            key = random.randint(1, 10000)
            skey = str(key)
            qr = QRCode()
            i = 0
            for val1 in val:
                i += 1
                print(val1)
                enc = cipher_helper.cipher("12345678", val1)
                print("Encrypted text:", enc)
                iname = skey + "img" + str(i)
                # 存儲 QR Code 圖片到本地
                qr.qr(enc, "path/to/your/image/directory/" + iname + ".png")

                # 假設將資料寫入本地檔案而不是 DB
                with open("path/to/your/data/directory/" + iname + ".txt", "w") as file:
                    file.write(f"Name: {name}\nID: {id}\nText: {val1}\nEncrypted: {enc}\nSecret Key: {skey}\n")

            print("Succesfully Splitted and Encrypted")

        except Exception as ex:
            print("An error occurred:", ex)

if __name__ == "__main__":
    text_to_process = "Your text here"  # 替換為要處理的文本
    message_processor = Message()
    message_processor.process_request(text_to_process)
