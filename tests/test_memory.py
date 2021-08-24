from models import Memory, Command


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
    assert mem.reads == 3 and mem.writes == 4
