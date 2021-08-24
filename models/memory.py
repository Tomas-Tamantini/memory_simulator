from typing import List

from models.command import Command


class Memory:
    def __init__(self):
        self.reads = 0
        self.writes = 0
        self.hits = 0
        self.misses = 0

    def execute(self, commands: List[Command]) -> str:
        for cmd in commands:
            self._execute_command(cmd)
        return ""

    def _execute_command(self, command: Command) -> None:
        if command.is_write:
            self.writes += 1
        else:
            self.reads += 1
