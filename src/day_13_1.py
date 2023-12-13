from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List

FILEPATH = '../data/day_13.txt'
TEST_FILEPATH = '../data/day_13_test.txt'


@dataclass
class Block:
    grid: List[str]
    mirror_type: str = 'Horizontal'  # Start with horizontal or vertical
    mirror_line: int | None = None

    def run(self):
        self.find_mirror()
        if self.mirror_line is None:
            self.invert_grid()
            self.find_mirror()

        if self.mirror_line is None:
            print('No mirror found')
        else:
            if self.mirror_type == 'Vertical':
                return self.mirror_line
            else:
                return 100 * self.mirror_line

    def invert_grid(self):
        inverted_grid = ['' for _ in range(0, len(self.grid[0]))]
        for line in self.grid:
            for i, token in enumerate(list(line)):
                inverted_grid[i] += token
        self.grid = inverted_grid
        self.mirror_type = 'Vertical' if self.mirror_type == 'Horizontal' else 'Horizontal'

    def find_mirror(self):
        for i in range(0, len(self.grid) - 1):
            if self.grid[i] == self.grid[i + 1]:
                if self._full_mirror_check(i):
                    self.mirror_line = i + 1
                    break

    def _full_mirror_check(self, line_nr):
        found_mirror = True
        n_rows = min(len(self.grid) - 1 - line_nr, line_nr + 1)
        for i in range(1, n_rows):
            if self.grid[line_nr - i] != self.grid[line_nr + 1 + i]:
                found_mirror = False
                break
        return found_mirror


def solve(data):
    data.append('')
    blocks = []
    block = []
    for line in data:
        if line == '':
            blocks.append(Block(block))
            block = []
        else:
            block.append(line)
    return sum([b.run() for b in blocks])


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
