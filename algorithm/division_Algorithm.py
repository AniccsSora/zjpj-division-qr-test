class DivisionAlgorithm:
    def __init__(self):
        self.text = ""         # 初始化文本
        self.max_count = 0    # 初始化最大字符數

    def set_values(self, text, max_count):
        self.text = text      # 設定文本內容
        self.max_count = max_count  # 設定最大字符數

    def get_process(self):
        div = len(self.text) // self.max_count
        remainder = len(self.text) % self.max_count
        size = div + 1 if remainder > 0 else div

        val = ["" for _ in range(size)]

        flag = 0
        count = self.max_count
        k = 0

        for k in range(size):
            line = ""
            if k == size - 1:
                count = len(self.text)
            for i in range(flag, count):
                line += self.text[i]
            flag += self.max_count
            count += self.max_count

            val[k] = line

        return val


def main():
    division_algorithm = DivisionAlgorithm()
    division_algorithm.set_values("This the test texttt abcccdd 1234", 5)  # 設定文本和最大字符數
    val = division_algorithm.get_process()
    for val1 in val:
        print(">{}<".format(val1))


if __name__ == "__main__":
    main()
