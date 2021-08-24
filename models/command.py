class Command:
    def __init__(self, is_write: bool):
        self.is_write = is_write


def decode_command(command: str) -> Command:
    is_write = command[2] == '1'
    return Command(is_write)
