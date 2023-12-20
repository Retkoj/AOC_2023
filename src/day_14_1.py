from argparse import ArgumentParser

FILEPATH = '../data/day_14.txt'
TEST_FILEPATH = '../data/day_14_test.txt'


def tilt_north(data):
    tilted = data
    still_moving = True
    while still_moving:
        still_moving = False
        for row in range(1, len(data)):
            for col in range(0, len(data[0])):
                if tilted[row][col] == 'O' and tilted[row - 1][col] == '.':
                    tilted[row - 1][col] = 'O'
                    tilted[row][col] = '.'
                    still_moving = True
    return tilted


def solve(data):
    data = [list(line) for line in data]
    tilted = tilt_north(data)
    print('\n'.join([''.join(row) for row in tilted]))
    load = len(tilted)
    result = 0
    for row in tilted:
        result += row.count('O') * load
        load -= 1
    print(sum([row.count('O') * (len(tilted) - i) for i, row in enumerate(tilted)]))
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
