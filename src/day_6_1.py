import re
from argparse import ArgumentParser

FILEPATH = '../data/day_6.txt'
TEST_FILEPATH = '../data/day_6_test.txt'


def solve(data):
    times = [int(n) for n in re.findall(r'(\d+)', data[0].split(':')[1])]
    distances = [int(n) for n in re.findall(r'(\d+)', data[1].split(':')[1])]
    result = 1

    for index, t in enumerate(times):
        possible_times = [i * (t - i) for i in range(0, t)]
        tmp = [1 if pt > distances[index] else 0 for pt in possible_times]
        result *= sum(tmp)
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
