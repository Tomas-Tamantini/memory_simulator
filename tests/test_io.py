from models.command import decode_command


def test_decode_write_command():
    cmd = "5 1 00000000000000000000000000000101"
    decoded_command = decode_command(cmd)
    assert decoded_command.is_write


def test_decode_read_command():
    cmd = "5 0"
    decoded_command = decode_command(cmd)
    assert not decoded_command.is_write
