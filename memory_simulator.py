import sys

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

    print(f'Output file saved - {OUTPUT_PATH}')


if __name__ == '__main__':
    args = sys.argv
    input_path = 'input_model.txt' if len(args) < 2 else args[1]
    if len(args) > 2 and 'c' in args[2].lower():
        print(f'Running MemorySimulator (C implementation) - Input file: {input_path}')
        # TODO: Run C implementation here
    else:
        print(f'Running MemorySimulator (Python implementation) - Input file: {input_path}')
        main(input_path)
