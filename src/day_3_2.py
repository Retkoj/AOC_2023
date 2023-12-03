import re
from argparse import ArgumentParser

import numpy as np

FILEPATH = '../data/day_3.txt'
TEST_FILEPATH = '../data/day_3_test.txt'


def solve(data):
    part_numbers = []
    numbers = {}
    signs = {}
    for i, line in enumerate(data):
        numbers[i] = {}
        for match in re.finditer(r'(\d+)', line):
            span = (match.span()[0] - 1, match.span()[1])
            numbers[i][span] = int(match.group())

        signs[i] = {}
        for match in re.finditer(r'[*]', line):
            signs[i][int(match.span()[0])] = []

    print(numbers)
    print(signs)

    for i in range(0, len(data)):
        for span, number in numbers[i].items():
            r = list(range(span[0], span[1] + 1))
            if i > 0:
                for star in [n for n in signs[i - 1].keys() if n in r]:
                    signs[i - 1][star].append(number)

            for star in [n for n in signs[i].keys() if n in r]:
                signs[i][star].append(number)

            if i < (len(data) - 1):
                for star in [n for n in signs[i + 1].keys() if n in r]:
                    signs[i + 1][star].append(number)

    gear_ratios = []
    for i in range(0, len(data)):
        gear_ratios += [np.prod(l) for l in signs[i].values() if len(l) == 2]
    print(gear_ratios)
    return sum(gear_ratios)


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
