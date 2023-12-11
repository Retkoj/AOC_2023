from argparse import ArgumentParser

FILEPATH = '../data/day_9.txt'
TEST_FILEPATH = '../data/day_9_test.txt'


def get_diff_serie(serie):
    new_serie = []
    for i in range(0, len(serie) - 1):
        new_serie.append(serie[i + 1] - serie[i])
    return new_serie


def solve(data):
    series = {}
    for i, line in enumerate(data):
        current_serie = [int(n) for n in line.split(' ')]
        series[i] = {}
        j = 0
        # all zeros gives false:
        while any(current_serie):
            series[i][j] = current_serie
            next_serie = get_diff_serie(current_serie)
            current_serie = next_serie
            j += 1

    print(series)
    result = 0
    n_series = len(series)
    for i in range(0, n_series):
        for j in range(len(series[i]) - 1, 0, -1):
            next_num = series[i][j - 1][-1] + series[i][j][-1]
            series[i][j - 1].append(next_num)
            if (j - 1) == 0:
                result += series[i][j - 1][-1]

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
