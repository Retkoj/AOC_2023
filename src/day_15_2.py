from argparse import ArgumentParser

FILEPATH = '../data/day_15.txt'
TEST_FILEPATH = '../data/day_15_test.txt'


class Hashmap:
    def __init__(self):
        self.hashmap = {key: [] for key in range(0, 256)}

    def initiate_map(self, lines):
        for line in lines:
            if '=' in line:
                label, focus_length = line.split('=')
                label_value = self.calculate_label(label)
                self.add_lens(label_value, label, int(focus_length))
            elif '-' in line:
                label = line[:-1]
                label_value = self.calculate_label(label)
                self.remove_from_map(label_value, label)

    def remove_from_map(self, label_value, label):
        lenses = self.hashmap[label_value]
        if label in [t[0] for t in lenses]:
            index = [t[0] for t in lenses].index(label)
            self.hashmap[label_value].pop(index)

    def add_lens(self, label_value, label, focus_length):
        lenses = self.hashmap[label_value]
        if label in [t[0] for t in lenses]:
            index = [t[0] for t in lenses].index(label)
            self.hashmap[label_value].pop(index)
            self.hashmap[label_value].insert(index, (label, focus_length))
        else:
            self.hashmap[label_value].append((label, focus_length))

    def calculate_label(self, label):
        tmp = 0
        for c in label:
            tmp += ord(c)
            tmp *= 17
            tmp = tmp % 256
        return tmp

    def calculate_focusing_power(self):
        results = []
        for i in range(0, 256):
            if self.hashmap[i]:
                results += [(i + 1) * (index + 1) * f_value
                            for index, f_value in enumerate([t[1] for t in self.hashmap[i]])]
        return sum(results)


def solve(data):
    lines = data[0].split(',')
    hashmap = Hashmap()
    hashmap.initiate_map(lines)
    return hashmap.calculate_focusing_power()


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
