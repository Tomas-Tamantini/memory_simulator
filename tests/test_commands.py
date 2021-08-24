import pytest

from models.load_commands import decode_command


@pytest.mark.parametrize('invalid_write_cmd', [
    "5 1 0000000000000000000000000000101",  # 31 bits of data (requires 32)
    "2  1  01000000000001110000000000000101 0000",  # Extra four bits
    "4096 1 00000000000000000000000000001011",  # Invalid address (max = 4095)
    "33 1",  # Missing data
    "4023  2  01000000000001110000000000000101",  # Bad read/write bit
    "2  1  01000200000001110000000340000101",  # Data can only have 0's and 1's
])
def test_decode_invalid_write_command(invalid_write_cmd):
    with pytest.raises(ValueError):
        decode_command(invalid_write_cmd)


@pytest.mark.parametrize('valid_write_cmd', [
    "5 1 00000000000000000000000000000101",
    "2  1  01000000000001110000000000000101",
    "\t0\t  1\t10000000000111110000000000000101\n",
])
def test_decode_valid_write_command(valid_write_cmd):
    decoded_command = decode_command(valid_write_cmd)
    assert decoded_command.is_write


@pytest.mark.parametrize('invalid_read_cmd', [
    "77 0 00000000000000000000000001000101",  # Read command should not have any data
    "5555 0",  # Invalid address (max = 4095)
])
def test_decode_invalid_read_command(invalid_read_cmd):
    with pytest.raises(ValueError):
        decode_command(invalid_read_cmd)


@pytest.mark.parametrize('valid_read_cmd', [
    "77 0",
    "1234 0",
    "\t  1234\t0   \n ",
])
def test_decode_valid_read_command(valid_read_cmd):
    cmd = "5 0"
    decoded_command = decode_command(cmd)
    assert not decoded_command.is_write
