from argparse import ArgumentParser

from shapely import Polygon, Point

FILEPATH = '../data/day_18.txt'
TEST_FILEPATH = '../data/day_18_test.txt'


def dig_hole(lines):
    starting_point = (0, 0)
    all_points = [starting_point]
    current_point = starting_point
    for line in lines:
        direction, steps, color = line.split(' ')
        steps = int(steps)
        if direction == 'R':
            all_points += [(current_point[0], current_point[1] + i) for i in range(1, steps + 1)]
        if direction == 'L':
            all_points += [(current_point[0], current_point[1] - i) for i in range(1, steps + 1)]
        if direction == 'U':
            all_points += [(current_point[0] - i, current_point[1]) for i in range(1, steps + 1)]
        if direction == 'D':
            all_points += [(current_point[0] + i, current_point[1]) for i in range(1, steps + 1)]
        current_point = all_points[-1]
    return all_points


def calibrate_hole(points):
    polygon = Polygon(points)
    bounds = polygon.bounds
    print(bounds)
    row_corr = 0 - bounds[0]
    col_corr = 0 - bounds[1]
    return [(int(row + row_corr), int(col + col_corr)) for row, col in points]


def print_points(points):
    polygon = Polygon(points)
    bounds = polygon.bounds
    print(bounds)
    grid = [['.'] * (int(bounds[3]) + 1) for _ in range(int(bounds[2]) + 1)]
    for row, col in points:
        grid[row][col] = '#'
    grid = [''.join(row) for row in grid]
    print('\n'.join(grid))


def points_in_polygon(points):
    polygon = Polygon(points)
    bounds = polygon.bounds
    all_points = [(row, col) for row in range(int(bounds[2] + 1)) for col in range(int(bounds[3]) + 1)]
    contained = [point for point in all_points if polygon.contains(Point(point))]
    contained = set(contained)
    contained.update(set(points))
    print(len(contained))
    return len(contained)


def solve(data):
    points = dig_hole(data)
    points = calibrate_hole(points)
    print_points(points)

    return points_in_polygon(points)


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
