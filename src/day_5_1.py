import re
from argparse import ArgumentParser

FILEPATH = '../data/day_5.txt'
TEST_FILEPATH = '../data/day_5_test.txt'


def parse_input(data):
    seeds = [int(n) for n in re.findall(r'(\d+)', data[0].split(':')[1])]
    print(seeds)
    stepmap = {}
    i = -1
    for line in data[2:]:
        if 'map' in line:
            i += 1
            stepmap[i] = {}
        elif line == '':
            pass
        else:
            dest, source, length = [int(n) for n in re.findall(r'(\d+)', line)]
            stepmap[i][(source, source + length + 1)] = dest

    return seeds, stepmap


def get_location(seed, stepmap):
    for i, ranges in stepmap.items():
        for source_range, dest in ranges.items():
            if seed in range(source_range[0], source_range[1]):
                size = seed - source_range[0]
                seed = dest + size
                break
    return seed


def solve(data):
    seeds, stepmap = parse_input(data)
    locations = []
    for seed in seeds:
        locations.append(get_location(seed, stepmap))
    return min(locations)


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
