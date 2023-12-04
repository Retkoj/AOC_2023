import re
from argparse import ArgumentParser

FILEPATH = '../data/day_4.txt'
TEST_FILEPATH = '../data/day_4_test.txt'


def solve(data):
    sets = {}
    for i, line in enumerate(data):
        tmp = line.split(':')[1]
        winning, scratched = tmp.split('|')
        winning = [int(n) for n in re.findall(r'(\d+)', winning)]
        scratched = [int(n) for n in re.findall(r'(\d+)', scratched)]
        if len(set(scratched)) != len(scratched):
            print("double numbers")

        n_wins = len(set(scratched).intersection(set(winning)))
        score = 1 if n_wins > 0 else 0
        if n_wins:
            for _ in range(0, n_wins - 1):
                score *= 2

        sets[i] = score
    return sum(sets.values())


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
