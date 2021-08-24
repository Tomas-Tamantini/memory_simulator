from models.command import Command


def decode_command(command: str) -> Command:
    command.replace('\t', ' ')
    elements = command.strip().split()

    if len(elements) < 2 or len(elements) > 3:
        _raise_decode_error('There should be 2 fields for read, and 3 fields for write, separated by spaces', command)

    address = _decode_address(elements[0], command)

    is_write = _decode_read_write_bit(elements[1], command)

    if is_write:
        if len(elements) != 3:
            _raise_decode_error('There should be exactly 3 fields in a write command', command)
        data = _decode_data(elements[2], command)
    else:
        if len(elements) != 2:
            _raise_decode_error('There should be exactly 2 fields in a read command', command)
        data = None
    return Command(address=address, is_write=is_write, data=data)


def _decode_address(address_as_str: str, command: str) -> int:
    try:
        address = int(address_as_str)
    except ValueError:
        _raise_decode_error('Invalid address', command)
    if address < 0 or address > 4095:
        _raise_decode_error('Invalid address. Must be a number between 0 and 4095', command)
    return address


def _decode_read_write_bit(bit_as_str: str, command: str) -> bool:
    if bit_as_str == '1':
        return True
    if bit_as_str == '0':
        return False
    _raise_decode_error('Invalid Read/Write bit', command)


def _decode_data(data_as_str, command: str) -> str:
    if len(data_as_str) != 32:
        _raise_decode_error('Data field of a write command should have 32 bits', command)
    if not set(data_as_str).issubset({'0', '1'}):
        _raise_decode_error("Data field can only have 0's and 1's", command)
    return data_as_str


def _raise_decode_error(error_msg: str, command: str):
    raise ValueError(f'Could not decode command: {command} - {error_msg}')
