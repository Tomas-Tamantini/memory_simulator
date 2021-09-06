from python_implementation import get_commands_from_input_file, Memory

OUTPUT_PATH = 'result.txt'


def main(input_file_path: str):
    # Initialize empty memory
    memory = Memory()

    # Load commands
    try:
        commands = get_commands_from_input_file(input_file_path)
    except ValueError as err:
        print(f'Error: {err}')
        return

    # Execute commands and save output log
    output_log = memory.execute(commands)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(output_log)


if __name__ == '__main__':
    # TODO: Read file name from argv
    main('python_implementation/tests/txt_tests/in5.txt')
