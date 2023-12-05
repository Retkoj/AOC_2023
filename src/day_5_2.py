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
            stepmap[i][(source, source + length)] = dest

    return seeds, stepmap


def get_location(seed, stepmap):
    unmapped_seeds = [seed]
    mapped_seeds = []
    for i, ranges in stepmap.items():
        mapped_seeds = []
        # (50, 98)
        for source_range, dest in ranges.items():
            start_source, end_source = source_range
            next_unmapped = []
            # (79, 83)
            for seed_range in unmapped_seeds:
                start_seed, end_seed = seed_range
                # if (part) in range:
                if start_seed <= end_source and end_seed >= start_source:
                    # 79 - 50 -> 29
                    offset = start_seed - start_source
                    # if start falls in range
                    if offset >= 0:
                        start_mapped = dest + offset
                    else:
                        start_mapped = dest
                        next_unmapped.append((start_seed, start_source - 1))

                    # 98 - 83 -> 15
                    offset = end_source - end_seed
                    # if end falls in range:
                    if offset >= 0:
                        end_mapped = dest + (end_source - start_source) - offset
                    else:
                        end_mapped = dest + (end_source - start_source)
                        next_unmapped.append((end_source + 1, end_seed))
                    mapped_seeds.append((start_mapped, end_mapped))
                else:
                    next_unmapped.append(seed_range)  # if not in range, keep as is

            unmapped_seeds = next_unmapped

        mapped_seeds += unmapped_seeds  # last unmapped, map to themselves e.g. 82 -> 82
        unmapped_seeds = mapped_seeds  # Mapped values are unmapped values for next round
    return mapped_seeds


def solve(data):
    seeds, stepmap = parse_input(data)
    i = 0
    n_seeds = len(seeds) / 2
    print(stepmap)
    locations = []
    while i < n_seeds:
        # inclusive end
        locations += get_location((seeds[i], seeds[i] + seeds[i + 1]), stepmap)
        # locations += get_location((82, 83), stepmap)
        i += 2
    print(locations)
    return min(locations)[0]


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
