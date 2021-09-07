class DataMemory:
    def __init__(self):
        self.__bytes = ['X' * 8 for _ in range(4095)]

    def write(self, address: int, word: str):
        for i in range(4):
            index = address + i
            if index < len(self.__bytes):
                self.__bytes[index] = word[8 * i:8 * (i + 1)]

    def read(self, address) -> str:
        data = ''
        first_addr = 16 * (address // 16)
        for i in range(first_addr, first_addr + 16):
            data += self.__bytes[i] if i < len(self.__bytes) else 'X' * 8
        return data
