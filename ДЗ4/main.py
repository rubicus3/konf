import re


class Assembler:
    def __init__(self, path_to_programm: str, path_to_binary: str):
        self.FREE_MEMORY_ADDRESS = -1
        self.NAMESPACE = {}
        self.INPUT_FILE = path_to_programm
        self.OUTPUT_FILE = path_to_binary

    def get_free_address(self):
        self.FREE_MEMORY_ADDRESS += 1
        return self.FREE_MEMORY_ADDRESS

    def add_var_to_namespace(self, var: str) -> int:
        ADDRESS = self.get_free_address()
        self.NAMESPACE[var] = ADDRESS
        return ADDRESS

    def paginate(self, num: int, length: int) -> str:
        return "0" * (length - len(bin(num)[2:])) + bin(num)[2:]

    def write_to_binary(self, bytes: bytes):
        with open(self.OUTPUT_FILE, 'ab') as f:
            f.write(bytes)

    def bin_constant(self, a: int, b: int, c: int) -> bytes:
        a, b, c = self.paginate(a, 3), self.paginate(b, 4), self.paginate(c, 28)
        text = a + b + c + "0" * 5
        return int(text, 2).to_bytes(5, "big")

    def bin_read(self, a: int, b: int, c: int) -> bytes:
        a, b, c = self.paginate(a, 3), self.paginate(b, 4), self.paginate(c, 4)
        text = a + b + c + "0" * 29
        return int(text, 2).to_bytes(5, "big")

    def bin_bitreverse(self, a: int, b: int, c: int) -> bytes:
        a, b, c = self.paginate(a, 3), self.paginate(b, 4), self.paginate(c, 4)
        text = a + b + c + "0" * 29
        return int(text, 2).to_bytes(5, "big")

    def run(self):
        lines = ""
        with open(self.INPUT_FILE, 'r') as f:
            lines = f.readlines()
        for line in lines:

            # Загрузка константы
            if re.match(r"[a-zA-Z][a-zA-Z0-9]*=[0-9]+", line):
                var, value = line.split('=')
                var, value = var.strip(), value.strip()
                value = int(value)
                address = self.add_var_to_namespace(var)
                binary = self.bin_constant(7, address, value)
                self.write_to_binary(binary)


            elif re.match(r"[a-zA-Z][a-zA-Z0-9]*=bitreverse\([a-zA-Z][a-zA-Z0-9]*\)", line):
                l = line.split("=")
                var1 = l[0].strip()
                var2 = l[1].replace("(", " ").replace(")", " ").split()[1].strip()

                if var2 not in self.NAMESPACE.keys():
                    raise Exception(f"Переменная '{var2}' не была объявлена.")

                if var1 not in self.NAMESPACE.keys():
                    address1 = self.add_var_to_namespace(var1)
                else:
                    address1 = self.NAMESPACE[var1]

                address2 = self.NAMESPACE[var2]
                text = "100" + self.translate(address1, 4) + self.translate(address2, 4)
                self.write_to_binary(text)

            # Чтение и запись в память
            elif re.match(r"[a-zA-Z][a-zA-Z0-9]*=[a-zA-Z][a-zA-Z0-9]*", line):
                var1, var2 = line.split('=')
                var1, var2 = var1.strip(), var2.strip()
                if var2 not in self.NAMESPACE.keys():
                    raise Exception(f"Переменная '{var2}' не была объявлена.")

                if var1 not in self.NAMESPACE.keys():
                    address1 = self.add_var_to_namespace(var1)
                else:
                    address1 = self.NAMESPACE[var1]
                address2 = self.NAMESPACE[var2]

                text = "010" + self.translate(address1, 4) + self.translate(address2, 4)
                self.write_to_binary(text)


class Interpreter:
    def __init__(self, path_to_binary: str):
        with open(path_to_binary, 'rb') as f:
            self.BINARY = [x for x in f.read()]
        print(self.BINARY)
        self.MEMORY = [0 for _ in range(16)]

    def run(self):
        i = 0
        while i < len(self.BINARY):
            command = self.BINARY[i:i+3]
            print(command)
            break


def main():
    assembler = Assembler("programm.txt", "result.bin")
    assembler.run()
    # interpreter = Interpreter("result.bin")
    # interpreter.run()


if __name__ == '__main__':
    main()
