import re


class Assembler:
    def __init__(self, path_to_programm: str, path_to_binary: str):
        self.FREE_MEMORY_ADDRESS = -1
        self.NAMESPACE = {}
        self.INPUT_FILE = path_to_programm
        self.OUTPUT_FILE = path_to_binary

    def get_free_memory(self):
        self.FREE_MEMORY_ADDRESS += 1
        return self.FREE_MEMORY_ADDRESS

    def add_var_to_namespace(self, var: str) -> int:
        ADDRESS = self.get_free_memory()
        self.NAMESPACE[var] = ADDRESS
        return ADDRESS

    def translate(self, num: int, length: int) -> str:
        print(num, length)
        return "0" * (length - len(bin(num)[2:])) + bin(num)[2:]

    def write_to_binary(self, text: str):
        print(text)

    def assembler(self):
        lines = ""
        with open(self.INPUT_FILE, 'r') as f:
            lines = f.readlines()
        for line in lines:

            # Загрузка константы
            if re.match(r"[a-zA-Z][a-zA-Z0-9]*=[0-9]+", line):
                var, value = line.split('=')
                value = int(value)
                address = self.add_var_to_namespace(var)
                text = "111" + self.translate(address, 6) + self.translate(value, 34)
                self.write_to_binary(text)

            # Чтение и запись в память
            elif re.match(r"[a-zA-Z][a-zA-Z0-9]*=[a-zA-Z][a-zA-Z0-9]*", line):
                print("Чтение и запись")
                # var1, var2 = line.split('=')
                # if var2 not in self.NAMESPACE.keys():
                #     address = self.add_var_to_namespace(var2)
                #     text = "111" + self.translate(address, 6) + self.translate(var1, 34)
                #     self.write_to_binary(text)
                # else:
                #     raise Exception(f"Переменная '{var2}' не была объявлена.")


            elif re.match(r"[a-zA-Z][a-zA-Z0-9]*=bitreverse\([a-zA-Z][a-zA-Z0-9]*\)", line):
                print("Чтение и запись bitreverse")

    def run(self):
        self.assembler()

def interpreter():
    pass


def main():
    assembler = Assembler("programm.txt", "result.bin")
    assembler.run()



if __name__ == '__main__':
    main()
