import zxing
from algorithm.cipherHelper import CipherHelper

class Merge:
    def process_request(self, request, response):
        try:
            response.setContentType("text/html;charset=UTF-8")
            out = response.getWriter()
            sc = request.getSession().getServletContext()
            session = request.getSession()

            email = session.getAttribute("email")
            name = request.getParameter("name")

            # con = new DB().fun()  # 請自行替換為適當的資料庫連接程式碼

            # 請自行實現資料庫查詢部分
            # query1 = con.prepareStatement("SELECT * FROM msg where rname='" + name + "'  ")
            # rs = query1.executeQuery()

            print("select * from msg where rname='" + name + "'")

            qr = zxing.BarCodeReader()
            content = ""
            skey = ""

            # 假設您有多個 QR Code 圖片的檔案路徑
            file_paths = [
                sc.getRealPath("images") + "\\" + "image1.png",
                sc.getRealPath("images") + "\\" + "image2.png"
            ]

            for file_path in file_paths:
                decoded_barcode = qr.decode(file_path)
                content += decoded_barcode.parsed
                skey = decoded_barcode.raw['TEXT']

            cipher_helper = CipherHelper("12345678")
            original_content = cipher_helper.decipher("12345678", content).strip()

            # 將解密後的內容保存到檔案或進行其他處理
            with open("output.txt", "w") as output_file:
                output_file.write(original_content)

            em = [email]
            session.setAttribute("key", skey)
            subject = "Your Secret key"
            message = "User Name  :" + name + "\nUser Key  :" + skey

            print("Message " + message)
            fr = "otpmessenger"  # without @gmail.com
            pw = "qawsedrftg"  # sender password

            # 請自行實現郵件發送部分
            # mail.sendFromGMail(fr, pw, em, subject, message)

            out.println("<script>"
                        + "alert('Merged Successfully')"
                        + "</script>")

            # 請自行處理 request 轉發部分
            # requestDispatcher = request.getRequestDispatcher("Merge.jsp")
            # requestDispatcher.include(request, response)

        except Exception as ex:
            print(ex)

    # 請自行實現 doGet 和 doPost 方法，根據您的應用需求進行處理