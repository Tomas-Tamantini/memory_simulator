from typing import List

from models.cache_memory import CacheMemory
from models.command import Command


class Memory:
    def __init__(self):
        self.reads = 0
        self.writes = 0
        self.hits = 0
        self.misses = 0
        self.__cache = CacheMemory()
        self.__log = []

    @property
    def hit_rate(self) -> float:
        return 0.0 if self.reads == 0 else self.hits / self.reads

    @property
    def miss_rate(self) -> float:
        return 0.0 if self.reads == 0 else self.misses / self.reads

    def execute(self, commands: List[Command]) -> str:
        for cmd in commands:
            self._execute_command(cmd)
        return self.header + '\n'.join(self.__log)

    def _execute_command(self, command: Command) -> None:
        if command.is_write:
            self.__cache.write(command.address, command.data)
            self.writes += 1
            out_char = 'W'
        else:
            is_hit = self.__cache.read(command.address)
            self.reads += 1
            if is_hit:
                out_char = 'H'
                self.hits += 1
            else:
                out_char = 'M'
                self.misses += 1

        self.__log.append(command.as_raw_str + ' ' + out_char)

    @property
    def header(self) -> str:
        return f'READS: {self.reads}\nWRITES: {self.writes}\nHITS: {self.hits}\nMISSES: {self.misses}\n' \
               f'HIT RATE: {self.hit_rate:.2f}\nMISS RATE: {self.miss_rate:.2f}\n\n'
