import re
from argparse import ArgumentParser
from math import lcm

FILEPATH = '../data/day_8.txt'
TEST_FILEPATH = '../data/day_8_2_test.txt'


def get_network(data):
    network = {}
    for line in data:
        points = re.findall(r'(\w+)', line)
        network[points[0]] = {'L': points[1], 'R': points[2]}

    return network


def solve(data):
    lr_instructions = data[0]
    network = get_network(data[2:])

    a_points = [point for point in network.keys() if list(point)[-1] == 'A']

    all_z_ends = False
    steps = 0
    i = 0

    z_steps = {}
    current_points = a_points
    while not all_z_ends:
        lr = lr_instructions[i]
        next_points = [network[current_point][lr] for current_point in current_points]
        steps += 1
        z_points = [True if list(p)[-1] == 'Z' else False for p in next_points]
        if all(z_points) or len(z_steps.keys()) == len(current_points):
            break
        if any(z_points):
            z_steps[z_points.index(True)] = steps
            print(f"step {steps}: {z_points}")
        current_points = next_points
        i += 1
        if i >= len(lr_instructions):
            i = 0
    print(z_steps)
    result = lcm(*list(z_steps.values()))

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
