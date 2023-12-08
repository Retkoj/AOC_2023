import re
from argparse import ArgumentParser

FILEPATH = '../data/day_8.txt'
TEST_FILEPATH = '../data/day_8_test.txt'


def get_network(data):
    network = {}
    for line in data:
        points = re.findall(r'(\w+)', line)
        network[points[0]] = {'L': points[1], 'R': points[2]}

    return network


def solve(data):
    lr_instructions = data[0]
    network = get_network(data[2:])

    steps = 0
    i = 0
    current_point = 'AAA'
    while current_point != 'ZZZ':
        lr = lr_instructions[i]
        current_point = network[current_point][lr]
        steps += 1
        i += 1
        if i >= len(lr_instructions):
            i = 0

    return steps


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
