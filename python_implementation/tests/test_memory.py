from python_implementation.models import Memory, Command
from python_implementation.models.load_commands import decode_command


def test_memory_initializes_empty():
    mem = Memory()
    assert mem.reads == mem.writes == mem.hits == mem.misses == 0


def test_read_command_increments_read_and_write_numbers():
    mem = Memory()
    commands = [
        Command(address=1, is_write=False),
        Command(address=13, is_write=True, data="1" * 32),
        Command(address=13, is_write=True, data="0" * 32),
        Command(address=999, is_write=False),
        Command(address=3000, is_write=True, data="1" * 32),
        Command(address=1555, is_write=False),
        Command(address=4000, is_write=True, data="1" * 32),
    ]
    mem.execute(commands)
    assert mem.reads == 3 and mem.writes == 4 and mem.misses + mem.hits == mem.reads


def test_execution():
    commands = """
        5 1 00000000000000000000000000000101
        5 0
        12 1 00000000000000000000000000010010
        25 0
    """
    decoded_commands = [decode_command(cmd) for cmd in commands.split('\n') if len(cmd.strip()) > 0]
    mem = Memory()
    mem.execute(decoded_commands)
    assert mem.reads == mem.writes == 2
    assert mem.hits == mem.misses == 1


