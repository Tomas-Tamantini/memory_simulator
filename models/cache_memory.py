class CacheMemory:
    def write(self, address: int, data: str) -> None:
        """Writes data to given address. If 'dirty' bit is set, writes back to data memory"""
        pass

    def read(self, address: int) -> bool:
        """Reads from given address. If it's a hit, returns True, and a miss returns False"""
        return True
