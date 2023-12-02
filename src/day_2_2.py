import re
from argparse import ArgumentParser

import numpy as np

FILEPATH = '../data/day_2.txt'
TEST_FILEPATH = '../data/day_2_test.txt'


def solve(data):
    games = {}
    powers = {}
    for game in data:
        id = int(re.match(r'\w+ (\d+)', game).group(1))
        games[id] = {'red': 0, 'green': 0, 'blue': 0}
        for turn in game.split(';'):
            matches = re.findall(r'(\d+) (\w+)', turn)
            for match in matches:
                if games[id][match[1]] < int(match[0]):
                    games[id][match[1]] = int(match[0])
        powers[id] = np.prod([value if value > 0 else 1 for value in games[id].values()])

    result = sum(powers.values())

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

    result = solve(input_data)
    print(f"{'-' * 100}\nOUTPUT: {result}")
