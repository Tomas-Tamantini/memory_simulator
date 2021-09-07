import sys
from subprocess import SubprocessError, call

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
    input_path = None
    run_c = False
    if len(args) > 1:
        if '.txt' in args[1].lower():
            input_path = args[1]
        elif 'c' in args[1].lower():
            run_c = True
    if len(args) > 2:
        input_path = args[2]

    if input_path is None:
        input_path = input('Informe o arquivo de entrada: ')

    if run_c:
        print(f'Running MemorySimulator (C implementation) - Input file: {input_path}')
        try:
            call(["c_implementation/MemSimulator.out", input_path])
            print('')
        except SubprocessError:
            main(input_path)
    else:
        print(f'Running MemorySimulator (Python implementation) - Input file: {input_path}')
        main(input_path)
