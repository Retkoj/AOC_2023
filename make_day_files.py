from argparse import ArgumentParser
from pathlib import Path


def create_file(file_path: Path):
    if file_path.exists():
        print(f'{file_path} already exists')
    else:
        with open(str(file_path), 'w+') as in_file:
            in_file.write('')
            print(f'Created file: {file_path}')


def make_day_files(day_number: str):
    """
    Creates:
      - ./src/day_[day_number]_1.py
      - ./src/day_[day_number]_2.py
      - ./data/day_[day_number].txt
      - ./data/day_[day_number]_test.txt

    The .py file is created with the template provided in ./stub.py

    :param day_number: number of the day
    """
    input_file = Path('./data') / f'day_{day_number}_test.txt'
    create_file(input_file)
    input_file = Path('./data') / f'day_{day_number}.txt'
    create_file(input_file)
    for i in [1, 2]:
        file_path = Path('./src') / f'day_{day_number}_{i}.py'
        if file_path.exists():
            print('{} already exists'.format(file_path))
        else:
            with (open(str(file_path), 'w+') as new_file,
                  open(str(Path().cwd() / 'stub.py'), 'r') as stub_file):
                for line in stub_file.readlines():
                    if line == 'FILEPATH = ""\n':
                        line = f"FILEPATH = '../data/day_{day_number}.txt'\n"
                    if line == 'TEST_FILEPATH = ""\n':
                        line = f"TEST_FILEPATH = '../data/day_{day_number}_test.txt'\n"
                    new_file.write(line)
                print(f'Created file {file_path}')


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument('day', type=int, help="Puzzle day, integer")
    args = argparser.parse_args()
    make_day_files(args.day)
