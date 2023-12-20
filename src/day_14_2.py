from argparse import ArgumentParser

FILEPATH = '../data/day_14.txt'
TEST_FILEPATH = '../data/day_14_test.txt'


def tilt_cycle(data):
    tilted = data
    for direction in ['N', 'W', 'S', 'E']:
        still_moving = True
        while still_moving:
            still_moving = False
            for row in range(0, len(data)):
                for col in range(0, len(data[0])):
                    if direction == 'N':
                        if (row - 1) >= 0 and tilted[row][col] == 'O' and tilted[row - 1][col] == '.':
                            tilted[row - 1][col] = 'O'
                            tilted[row][col] = '.'
                            still_moving = True
                    if direction == 'W':
                        if tilted[row][col] == 'O' and (col - 1) >= 0 and tilted[row][col - 1] == '.':
                            tilted[row][col - 1] = 'O'
                            tilted[row][col] = '.'
                            still_moving = True
                    if direction == 'S':
                        r = len(data) - 1 - row  # 15, 14, ..
                        if tilted[r][col] == 'O' and (r + 1) < len(data) and tilted[r + 1][col] == '.':
                            tilted[r + 1][col] = 'O'
                            tilted[r][col] = '.'
                            still_moving = True
                    if direction == 'E':
                        if tilted[row][col] == 'O' and (col + 1) < len(data[0]) and tilted[row][col + 1] == '.':
                            tilted[row][col + 1] = 'O'
                            tilted[row][col] = '.'
                            still_moving = True
    return tilted


def solve(data):
    data = [list(line) for line in data]
    pattern = {}
    # 300 / 2 = 150 should be enough to capture the repeating pattern
    for i in range(0, 300):
        tilted = tilt_cycle(data)
        tmp = sum([row.count('O') * (len(tilted) - i) for i, row in enumerate(tilted)])
        pattern[i] = tmp

    # start looking for a repeating pattern halfway through the set:
    right_side = list(pattern.values())[(len(pattern.values()) // 2) + 1:]
    # Since a pattern can have repeating values next to each other, assume a minimum pattern length of 5
    minimum_pattern_length = 5
    actual_pattern_length = 5
    actual_pattern = right_side[:minimum_pattern_length]
    while True:
        # if the sequence is repeating itself (with at least 5 values), break
        if (len(actual_pattern) > minimum_pattern_length and
                actual_pattern[-minimum_pattern_length:] == actual_pattern[:minimum_pattern_length]):
            break
        # otherwise keep adding values to the pattern
        actual_pattern += [right_side[actual_pattern_length]]
        actual_pattern_length += 1

    actual_pattern_length = len(actual_pattern[:-5])

    # take the first index of the split (+1 for zero index correction), subtract it from the goal and get the
    # remainder by dividing by pattern length. This gives the index in the pattern sequence for 1000000000
    pattern_index = (1000000000 - ((len(pattern.values()) // 2) + 2)) % actual_pattern_length
    print(f"pattern_length: {actual_pattern_length} \npattern: {actual_pattern[:-5]} \n"
          f"pattern index for 1000000000th value: {pattern_index}")

    return actual_pattern[pattern_index]


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
