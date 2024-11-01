import re
import yaml


class Assembler:
    def __init__(self, path_to_programm: str, path_to_binary: str, path_to_log_file):
        self.FREE_MEMORY_ADDRESS = -1
        self.NAMESPACE = {}
        self.INPUT_FILE = path_to_programm
        self.OUTPUT_FILE = path_to_binary
        self.LOG_FILE = path_to_log_file
        open(self.OUTPUT_FILE, 'w').close()
        open(self.LOG_FILE, 'w').close()

        self.LOG_ARRAY = []

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
        logged = ", ".join([("0x" + hex(i)[2:]).ljust(4, '0') for i in bytes])
        self.log({"bin": logged}, method="append")

        with open(self.OUTPUT_FILE, 'ab') as f:
            f.write(bytes)

    def bin_constant(self, a: int, b: int, c: int) -> bytes:
        self.log({"A": a, "B": b, "C": c})

        a, b, c = self.paginate(a, 3), self.paginate(b, 4), self.paginate(c, 28)
        text = a + b + c + "0" * 5
        return int(text, 2).to_bytes(5, "big")

    def bin_read(self, a: int, b: int, c: int) -> bytes:
        self.log({"A": a, "B": b, "C": c})

        a, b, c = self.paginate(a, 3), self.paginate(b, 4), self.paginate(c, 4)
        text = a + b + c + "0" * 29
        return int(text, 2).to_bytes(5, "big")

    def bin_shift(self, a: int, b: int, c: int, d: int):
        self.log({"A": a, "B": b, "C": c, "D": d})

        a, b, c, d = self.paginate(a, 3), self.paginate(b, 4), self.paginate(c, 5), self.paginate(d, 4)
        text = a + b + c + d + "0" * 24
        return int(text, 2).to_bytes(5, "big")

    def bin_bitreverse(self, a: int, b: int, c: int, d: int) -> bytes:
        self.log({"A": a, "B": b, "C": c, "D": d})

        a, b, c, d = self.paginate(a, 3), self.paginate(b, 4), self.paginate(c, 5), self.paginate(d, 4)
        text = a + b + c + d + "0" * 24
        return int(text, 2).to_bytes(5, "big")

    def log(self, text: dict, method="last"):
        if method == "last":
            self.LOG_ARRAY.append(text)
        elif method == "append":
            self.LOG_ARRAY[-1].update(text)

    def dump_log(self):
        with open(self.LOG_FILE, 'a') as f:
            yaml.dump(self.LOG_ARRAY, f)

    def run(self):
        with open(self.INPUT_FILE, 'r') as f:
            lines = f.readlines()
        for line in lines:
            # Загрузка константы
            if line.startswith("set"):
                _, var, value = line.split()
                var, value = var.strip(), int(value.strip())

                address = self.add_var_to_namespace(var)
                binary = self.bin_constant(7, address, value)
                self.write_to_binary(binary)

            # Чтение и запись в памяти
            elif line.startswith("mov"):
                _, var1, var2 = line.split()
                var1, var2 = var1.strip(), var2.strip()

                if var2 not in self.NAMESPACE.keys():
                    raise Exception(f"Переменная '{var2}' не была объявлена.")

                if var1 not in self.NAMESPACE.keys():
                    address1 = self.add_var_to_namespace(var1)
                else:
                    address1 = self.NAMESPACE[var1]
                address2 = self.NAMESPACE[var2]

                binary = self.bin_read(3, address1, address2)
                self.write_to_binary(binary)

            # Чтение из памяти и запись по адресу со сдвигом
            elif line.startswith("shift"):
                _, var1, shift, var2 = line.split()
                var1, shift, var2 = var1.strip(), int(shift.strip()), var2.strip()

                if var2 not in self.NAMESPACE.keys():
                    raise Exception(f"Переменная '{var2}' не была объявлена.")
                if var1 not in self.NAMESPACE.keys():
                    address1 = self.add_var_to_namespace(var1)
                else:
                    address1 = self.NAMESPACE[var1]

                address2 = self.NAMESPACE[var2]
                binary = self.bin_shift(1, address1, shift, address2)
                self.write_to_binary(binary)

            # Унарная операция bitreverse
            elif line.startswith("bitreverse"):
                _, var1, shift, var2 = line.split()
                var1, shift, var2 = var1.strip(), int(shift.strip()), var2.strip()

                if var2 not in self.NAMESPACE.keys():
                    raise Exception(f"Переменная '{var2}' не была объявлена.")
                if var1 not in self.NAMESPACE.keys():
                    address1 = self.add_var_to_namespace(var1)
                else:
                    address1 = self.NAMESPACE[var1]

                address2 = self.NAMESPACE[var2]
                binary = self.bin_bitreverse(4, address1, shift, address2)
                self.write_to_binary(binary)
        self.dump_log()


class Interpreter:
    def __init__(self, path_to_binary: str, path_to_result):
        with open(path_to_binary, 'rb') as f:
            self.BINARY = f.read()
        self.MEMORY = [0 for _ in range(16)]
        self.RESULT_FILE = path_to_result
        open(self.RESULT_FILE, 'w').close()

    def run(self):
        bits = bin(int.from_bytes(self.BINARY))[2:]
        commands = [bits[i:i+5*8] for i in range(0, len(bits), 8*5)]

        for command in commands:
            command_type = command[0:3]
            if command_type == "111":
                address = int(command[3:7], 2)
                value = int(command[7:35], 2)
                self.MEMORY[address] = value
            elif command_type == "011":
                address1 = int(command[3:7], 2)
                address2 = int(command[7:11], 2)
                self.MEMORY[address1] = self.MEMORY[address2]

            elif command_type == "001":
                address1 = int(command[3:7], 2)
                shift = int(command[7:12], 2)
                address2 = int(command[12:16], 2)
                self.MEMORY[address1 + shift] = self.MEMORY[address2]

            elif command_type == "100":
                address1 = int(command[3:7], 2)
                shift = int(command[7:12], 2)
                address2 = int(command[12:16], 2)

                value = self.MEMORY[address2]
                reversed = int(bin(value)[2:].zfill(28)[::-1], 2)
                self.MEMORY[address1 + shift] = reversed

        self.log_result()

    def log_result(self):
        data = []
        for i in range(len(self.MEMORY)):
            data.append({"0b" + bin(i)[2:].zfill(4): self.MEMORY[i]})
        with open(self.RESULT_FILE, 'a') as f:
            yaml.dump(data, f)


def main():
    assembler = Assembler("programm.txt", "assembled.bin", "assembler_log.yaml")
    assembler.run()

    interpreter = Interpreter("assembled.bin", "result.yaml")
    interpreter.run()


if __name__ == '__main__':
    main()
