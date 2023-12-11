import re
from argparse import ArgumentParser

FILEPATH = '../data/day_11.txt'
TEST_FILEPATH = '../data/day_11_test.txt'


class Universe:
    def __init__(self, data):
        self.grid = []
        self.expand_universe(data)
        self.galaxy_locations = {}
        self.find_galaxies()
        self.galaxy_distances = {}
        self.find_distances()

    def expand_universe(self, data):
        tmp = []
        for line in data:
            tmp.append(line)
            if len(re.findall('#', line)) == 0:
                tmp.append(line)

        self.grid = [list(line) for line in tmp]
        empty_cols = []
        for col in range(0, len(self.grid[0])):
            empty_col = True
            for row in range(0, len(self.grid)):
                if self.grid[row][col] == '#':
                    empty_col = False
                    break
            if empty_col:
                empty_cols.append(col)
        print(empty_cols)
        for offset, col in enumerate(empty_cols):
            for row in range(0, len(self.grid)):
                self.grid[row].insert(col + offset, '.')

    def find_galaxies(self):
        i = 0
        for row_nr, row in enumerate(self.grid):
            for col, token in enumerate(row):
                if token == '#':
                    self.galaxy_locations[i] = (row_nr, col)
                    i += 1

    def find_distances(self):
        for key, location in self.galaxy_locations.items():
            for other_key, other_location in self.galaxy_locations.items():
                dist_key = tuple(sorted([key, other_key]))
                if key != other_key and dist_key not in self.galaxy_distances.keys():
                    self.galaxy_distances[dist_key] = sum([abs(a - b) for a, b in zip(location, other_location)])

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))


def solve(data):
    universe = Universe(data)
    return sum(universe.galaxy_distances.values())


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
