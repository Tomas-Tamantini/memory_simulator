from models import Memory


def test_memory_initializes_empty():
    mem = Memory()
    assert mem.reads == mem.writes == mem.hits == mem.misses == 0
