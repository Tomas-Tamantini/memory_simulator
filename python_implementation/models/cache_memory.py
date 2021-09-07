from typing import Tuple

from python_implementation.models.data_memory import DataMemory

# Masks
BYTE_OFFSET_MASK = 3  # 0000 0000 0000 0000 0000 0000 0000 0011
BLOCK_OFFSET_MASK = 12  # 0000 0000 0000 0000 0000 0000 0000 1100
BLOCK_INDEX_MASK = 1008  # 0000 0000 0000 0000 0000 0011 1111 0000
TAG_MASK = 3072  # 0000 0000 0000 0000 0000 1100 0000 0000
SPATIAL_ADDRESS_MASK = 4080  # 0000 0000 0000 0000 0000 1111 1111 0000


def destructure_address(address: int) -> Tuple[int, int, int, int, int]:
    """Returns byte offset, block offset, block index, tag and spatial address from address"""
    byte_offset = address & BYTE_OFFSET_MASK
    block_offset = (address & BLOCK_OFFSET_MASK) // 4
    block_index = (address & BLOCK_INDEX_MASK) // 16
    tag = (address & TAG_MASK) // 1024
    spatial_address = (address & SPATIAL_ADDRESS_MASK)
    return byte_offset, block_offset, block_index, tag, spatial_address


class Block:
    def __init__(self):
        self.is_dirty = False
        self.is_valid = False
        self.tag = 0

    def write(self, tag, data, block_offset):
        # TODO:
        # If block is not valid, fetch 128 bits from memory
        # Write 32 bits from data
        self.tag = tag
        self.is_valid = True
        self.is_dirty = True


class CacheMemory:
    def __init__(self):
        self.__data_memory = DataMemory()
        self.__blocks = [Block() for _ in range(64)]

    def write(self, address: int, data: str) -> None:
        """Writes data to given address. If 'dirty' bit is set, writes back to data memory"""
        _, word_index, block_index, tag, spatial_address = destructure_address(address)
        block = self.__blocks[block_index]
        if block.is_dirty and block.tag != tag:
            self.__write_back(block)
        block.write(tag, data, word_index)

    def read(self, address: int) -> bool:
        """Reads from given address. If it's a hit, returns True, and a miss returns False"""
        _, word_index, block_index, tag, spatial_address = destructure_address(address)
        block = self.__blocks[block_index]
        if block.is_valid and block.tag == tag:
            return True  # Is hit
        if block.is_dirty:
            self.__write_back(block)
        block.tag = tag
        self.__read_from_memory(block, address)
        return False

    def __write_back(self, block: Block):
        # TODO: Implement this method
        block.is_valid = True
        block.is_dirty = False

    def __read_from_memory(self, block: Block, address: int):
        # TODO: Implement this method
        block.is_valid = True
        block.is_dirty = False
