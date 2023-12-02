import re
from argparse import ArgumentParser

FILEPATH = '../data/day_2.txt'
TEST_FILEPATH = '../data/day_2_test.txt'


def solve(data, max_values: dict):
    games = {}
    for game in data:
        id = int(re.match(r'\w+ (\d+)', game).group(1))
        games[id] = True
        for turn in game.split(';'):
            matches = re.findall(r'(\d+) (\w+)', turn)
            for match in matches:
                if max_values[match[1]] < int(match[0]):
                    games[id] = False
                    break
            if not games[id]:
                break

    result = sum([id if value else 0 for id, value in games.items()])

    return result


def read_file(file_path):
    with open(file_path) as file:
        data = [i.strip('\n') for i in file.readlines()]

    print(f"INPUT DATA:\n{file_path}\n{data}\n")
    return data


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument('--input-file', type=str, required=False,
                           help="Path to the input file to process. Overwrites the filepath in the script.")
    argparser.add_argument('--test', action='store_true',
                           help="Run the script on the test file (data/day_[n]_test.txt), overwrites --input-file")
    args = argparser.parse_args()
    if args.input_file:
        FILEPATH = args.input_file
    if args.test:
        FILEPATH = TEST_FILEPATH

    input_data = read_file(FILEPATH)
    max_values = {'red': 12, 'green': 13, 'blue': 14}
    result = solve(input_data, max_values)
    print(f"{'-' * 100}\nOUTPUT: {result}")
