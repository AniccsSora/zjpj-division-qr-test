class GFG:
    def divide_string(self, text, n):
        str_size = len(text)
        part_size = str_size // n

        for i in range(str_size):
            if i % part_size == 0 and i != 0:
                print()
            print(text[i], end='')

if __name__ == "__main__":
    text = "Hi Good morning how are you"
    gfg = GFG()
    gfg.divide_string(text, 5)
