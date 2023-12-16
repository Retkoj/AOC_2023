from argparse import ArgumentParser
from collections import deque

FILEPATH = '../data/day_16.txt'
TEST_FILEPATH = '../data/day_16_test.txt'


class MirrorField:
    def __init__(self, field):
        self.field = field
        self.start = (0, 0)
        self.activated_spots = set()
        self.tokens = ['-', '|', '/', '\\']
        self.queue = deque()
        self.seen = set()

    def track_beam(self):
        self.queue.append((self.start, 'right'))
        while len(self.queue) > 0:
            next_item = self.queue.popleft()
            if next_item not in self.seen:
                self.seen.add(next_item)
                spot, direction = next_item
                match direction:
                    case 'up':
                        self.move_up(spot)
                    case 'down':
                        self.move_down(spot)
                    case 'left':
                        self.move_left(spot)
                    case 'right':
                        self.move_right(spot)
        self.print_activated()
        return len(self.activated_spots)

    def print_activated(self):
        grid = [['.'] * len(self.field[0]) for _ in range(0, len(self.field))]
        for row, col in self.activated_spots:
            grid[row][col] = '#'
        grid = [''.join(row) for row in grid]
        print('\n'.join(grid))

    def move_right(self, current_spot):
        for col in range(current_spot[1], len(self.field[0])):
            next_spot = (current_spot[0], col)
            self.activated_spots.add(next_spot)
            token = self.field[current_spot[0]][col]
            if next_spot == self.start or next_spot != current_spot:
                match token:
                    case '|':
                        self.queue.append((next_spot, 'up'))
                        self.queue.append((next_spot, 'down'))
                        return
                    case '/':
                        self.queue.append((next_spot, 'up'))
                        return
                    case '\\':
                        self.queue.append((next_spot, 'down'))
                        return
        return

    def move_up(self, current_spot):
        for row in range(current_spot[0] - 1, -1, -1):
            next_spot = (row, current_spot[1])
            self.activated_spots.add(next_spot)
            token = self.field[row][current_spot[1]]
            if next_spot == self.start or next_spot != current_spot:
                match token:
                    case '-':
                        self.queue.append((next_spot, 'right'))
                        self.queue.append((next_spot, 'left'))
                        return
                    case '/':
                        self.queue.append((next_spot, 'right'))
                        return
                    case '\\':
                        self.queue.append((next_spot, 'left'))
                        return
        return

    def move_left(self, current_spot):
        for col in range(current_spot[1] - 1, -1, -1):
            next_spot = (current_spot[0], col)
            self.activated_spots.add(next_spot)
            token = self.field[current_spot[0]][col]
            if next_spot == self.start or next_spot != current_spot:
                match token:
                    case '|':
                        self.queue.append((next_spot, 'up'))
                        self.queue.append((next_spot, 'down'))
                        return
                    case '/':
                        self.queue.append((next_spot, 'down'))
                        return
                    case '\\':
                        self.queue.append((next_spot, 'up'))
                        return
        return

    def move_down(self, current_spot):
        for row in range(current_spot[0] + 1, len(self.field)):
            next_spot = (row, current_spot[1])
            self.activated_spots.add(next_spot)
            token = self.field[row][current_spot[1]]
            if next_spot == self.start or next_spot != current_spot:
                match token:
                    case '-':
                        self.queue.append((next_spot, 'right'))
                        self.queue.append((next_spot, 'left'))
                        return
                    case '/':
                        self.queue.append((next_spot, 'left'))
                        return
                    case '\\':
                        self.queue.append((next_spot, 'right'))
                        return
        return


def solve(data):
    mirror_field = MirrorField(data)

    return mirror_field.track_beam()


def read_file(file_path):
    with open(file_path) as file:
        data = [i.strip('\n') for i in file.readlines()]

    print(f"INPUT DATA:\n{file_path}\n")
    print('\n'.join(data))
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
