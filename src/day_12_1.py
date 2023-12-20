import re
from argparse import ArgumentParser
from itertools import combinations
from math import factorial

FILEPATH = '../data/day_12.txt'
TEST_FILEPATH = '../data/day_12_test.txt'


def binomial_coef(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))


def find_arrangements(springs, goal):
    min_length = sum(goal) + len(goal) - 1
    spaces_left = len(springs) - min_length
    all_arrangements_indexes = combinations(range(len(goal) + spaces_left), len(goal))
    all_arrangements = []
    print(f"springs: {springs}  goal: {goal}")
    for indexes in all_arrangements_indexes:
        spans = zip(indexes, goal)
        tmp = ['.'] * len(springs)
        current_index = 0
        prev_index = 0
        for start, length in spans:
            current_index += (start - prev_index)
            tmp = ['#' if i in range(current_index, current_index + length) else token for i, token in enumerate(tmp)]
            current_index += length
            prev_index = start
        all_arrangements.append(''.join(tmp))
    return all_arrangements


def find_fitting_arrangements(all_arrangements, actual_line):
    possibles = []
    for possible_arrangement in all_arrangements:
        compared = [True if p == '.' and a in ['.', '?'] or p == '#' and a in ['#', '?'] else False
                    for p, a in zip(possible_arrangement, actual_line)]
        if all(compared):
            possibles.append(possible_arrangement)
    print(possibles)
    return len(possibles)


def solve(data):
    result = 0
    for line in data:
        springs, goal = line.split(' ')
        goal = [int(n) for n in re.findall(r'(\d+)', goal)]
        all_arrangements = find_arrangements(springs, goal)
        result += find_fitting_arrangements(all_arrangements, line)
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
