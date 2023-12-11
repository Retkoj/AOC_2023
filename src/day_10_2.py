from argparse import ArgumentParser

from shapely import Polygon, Point

FILEPATH = '../data/day_10.txt'
TEST_FILEPATH = '../data/day_10_test.txt'


class MainLoop:
    def __init__(self, data):
        self.grid = [list(row) for row in data]
        self.starting_point = self.find_start()
        self.full_path = []
        self.find_full_path()

    def find_start(self):
        for i, row in enumerate(self.grid):
            if 'S' in row:
                return i, row.index('S')

    def is_valid_coordinate(self, coordinate):
        """Within bounds and not yet in full_path"""
        return ((0 <= coordinate[0] < len(self.grid)) and
                (0 <= coordinate[1] < len(self.grid[0])) and
                (coordinate not in self.full_path))

    def get_valid_directions(self, token):
        match token:
            case 'L':
                return ['E', 'N']
            case '-':
                return ['E', 'W']
            case 'J':
                return ['W', 'N']
            case '7':
                return ['S', 'W']
            case 'S':
                return ['E', 'N', 'S', 'W']
            case '|':
                return ['S', 'N']
            case 'F':
                return ['S', 'E']

    def find_full_path(self):
        cr, cc = self.starting_point
        self.full_path.append(self.starting_point)
        neighbouring_coordinates = {'E': (0, 1), 'S': (1, 0), 'N': (-1, 0), 'W': (0, -1)}
        while True:
            valid_count = 0
            prev_token = self.grid[cr][cc]
            valid_directions = self.get_valid_directions(prev_token)
            for direction, point in neighbouring_coordinates.items():
                if direction in valid_directions:
                    nr, nc = (cr + point[0], cc + point[1])
                    if self.is_valid_coordinate((nr, nc)):
                        if ((direction == 'E' and self.grid[nr][nc] in ['J', '7', '-'])
                                or (direction == 'S' and self.grid[nr][nc] in ['J', '|', 'L'])
                                or (direction == 'N' and self.grid[nr][nc] in ['F', '|', '7'])
                                or (direction == 'W' and self.grid[nr][nc] in ['F', 'L', '-'])):
                            self.full_path.append((nr, nc))
                            cr, cc = nr, nc
                            valid_count += 1
                            break
            if valid_count == 0:
                break

    def find_trapped_points(self):
        poly_path = Polygon([Point(p) for p in self.full_path])
        tmp = [[(i, col) for col in range(0, len(row))] for i, row in enumerate(self.grid)]
        all_points = []
        for points in tmp:
            all_points += points
        min_row, min_col, max_row, max_col = poly_path.bounds

        relevant_points = [(r, c) for r, c in all_points if min_row <= r <= max_row and min_col <= c <= max_col and
                           (r, c) not in self.full_path]

        trapped_points = [point for point in relevant_points if poly_path.contains(Point(point))]
        return len(trapped_points)


def solve(data):
    main_loop = MainLoop(data)

    return main_loop.find_trapped_points()


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
