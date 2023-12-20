import re
from argparse import ArgumentParser

FILEPATH = '../data/day_19.txt'
TEST_FILEPATH = '../data/day_19_test.txt'


class Rules:
    def __init__(self, data):
        self.data = data
        self.rules = {}
        self.parse_data()

    def parse_data(self):
        for line in self.data:
            id, rules = line.split('{')
            rules = rules[:-1].split(',')
            self.rules[id] = rules

    def apply_rule(self, part, rule_id):
        rules = self.rules[rule_id]
        for rule in rules[:-1]:
            letter, sign, number, return_value = re.findall(r'([xmas])([<>])(\d+):(\w+)', rule)[0]
            number = int(number)
            condition = (part[letter] < number) if sign == '<' else (part[letter] > number)
            if condition:
                return return_value
        return rules[-1]


def parse_data(data):
    rule_data = []
    i = 0
    while True:
        if data[i] == '':
            i += 1
            break
        rule_data.append(data[i])
        i += 1
    rules = Rules(rule_data)

    parts = {}
    for key, values in enumerate(data[i:]):
        part_values = re.findall(r'([xmas])=(\d+)', values)
        parts[key] = {letter: int(value) for letter, value in part_values}

    return rules, parts


def solve(data):
    accepted_parts = []
    rules, parts = parse_data(data)
    for part_id, part in parts.items():
        current_rule = 'in'
        while True:
            current_rule = rules.apply_rule(part, current_rule)
            if current_rule in ['R', 'A']:
                if current_rule == 'A':
                    accepted_parts.append(part_id)
                break
    result = 0
    print(accepted_parts)
    for part_id in accepted_parts:
        result += sum(parts[part_id].values())

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
