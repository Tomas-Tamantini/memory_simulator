from models import get_commands_from_input_file


def main(input_file_path: str):
    try:
        commands = get_commands_from_input_file(input_file_path)
    except ValueError as err:
        print(f'Error: {err}')
        return


if __name__ == '__main__':
    # TODO: Read file name from argv
    main('input_model.txt')
