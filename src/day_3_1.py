import re
from argparse import ArgumentParser

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
        for match in re.finditer(r'[^a-zA-Z0-9\.]', line):
            signs[i][int(match.span()[0])] = match.group()

    print(numbers)
    print(signs)

    for i in range(0, len(data)):
        for span, number in numbers[i].items():
            r = list(range(span[0], span[1] + 1))
            if ((i > 0 and any([n in r for n in signs[i - 1].keys()])) or
                    (any([n in r for n in signs[i].keys()])) or
                    (i < (len(data) - 1) and any([n in r for n in signs[i + 1].keys()]))):
                part_numbers.append(number)

    print(part_numbers)
    return sum(part_numbers)


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
