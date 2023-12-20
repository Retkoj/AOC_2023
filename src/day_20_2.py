from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from math import lcm
from queue import Queue

FILEPATH = '../data/day_20.txt'
TEST_FILEPATH = '../data/day_20_test.txt'


class Pulse(Enum):
    LOW = 0
    HIGH = 1


@dataclass
class FlipFlop:
    name: str
    destinations: list
    status: bool = False

    def process_pulse(self, source: str, pulse: Pulse):
        if pulse == Pulse.LOW:
            self.status = not self.status
            return self.send_pulses()
        return []

    def send_pulses(self):
        pulse = Pulse.HIGH if self.status else Pulse.LOW
        destination_queue = []
        for destination in self.destinations:
            destination_queue.append((destination, pulse, self.name))
        return destination_queue


@dataclass
class Conjunction:
    name: str
    input_modules: dict
    destinations: list

    def process_pulse(self, source: str, pulse: Pulse):
        self.input_modules[source] = pulse
        return self.send_pulses()

    def send_pulses(self):
        pulse = Pulse.LOW if all([value == Pulse.HIGH for value in self.input_modules.values()]) else Pulse.HIGH
        destination_queue = []
        for destination in self.destinations:
            destination_queue.append((destination, pulse, self.name))
        return destination_queue


@dataclass
class Broadcaster:
    name: str
    destinations: list
    pulse: Pulse = Pulse.LOW

    def process_pulse(self, source: str, pulse: Pulse):
        self.pulse = pulse
        return self.send_pulses()

    def send_pulses(self):
        destination_queue = []
        for destination in self.destinations:
            destination_queue.append((destination, self.pulse, self.name))
        return destination_queue


def parse_modules(data):
    modules = {}
    conjunction_modules = []
    for line in data:
        source, destinations = line.split(' -> ')
        destinations = [d.strip() for d in destinations.split(',')]
        if source == 'broadcaster':
            modules['broadcaster'] = Broadcaster('broadcaster', destinations)
        elif source[0] == '%':
            modules[source[1:]] = FlipFlop(source[1:], destinations)
        elif source[0] == '&':
            modules[source[1:]] = Conjunction(source[1:], {}, destinations)
            conjunction_modules.append(source[1:])

    for module_name, module in modules.items():
        for destination in module.destinations:
            if destination in conjunction_modules:
                modules[destination].input_modules[module_name] = Pulse.LOW

    return modules


def process_pulses(modules, round, parent_module, lcm_factors):
    queue = Queue()
    queue.put(('broadcaster', Pulse.LOW, 'button'))
    low_count = 0
    high_count = 0
    while not queue.empty():
        destination, pulse, source = queue.get()
        if any([p == Pulse.HIGH for p in modules[parent_module].input_modules.values()]):
            for mod in [key for key, p in modules[parent_module].input_modules.items() if p == Pulse.HIGH]:
                lcm_factors[mod] = round if lcm_factors[mod] is None else lcm_factors[mod]

        if modules.get(destination, False):
            next_queue_items = modules[destination].process_pulse(source, pulse)
            [queue.put(item) for item in next_queue_items]
        if pulse == Pulse.LOW:
            low_count += 1
        elif pulse == Pulse.HIGH:
            high_count += 1

    return low_count, high_count, modules, lcm_factors


def solve(data):
    modules = parse_modules(data)
    low_count, high_count = 0, 0
    round = 1
    parent_module = [module for module_name, module in modules.items() if 'rx' in module.destinations]
    if len(parent_module) == 1 and type(parent_module[0]) == Conjunction:
        lcm_factors = {name: None for name in parent_module[0].input_modules.keys()}

        while True:
            low, high, modules, lcm_factors = process_pulses(modules, round, parent_module[0].name, lcm_factors)
            low_count += low
            high_count += high
            if all([v is not None for v in lcm_factors.values()]):
                break
            round += 1
        result = lcm(*list(lcm_factors.values()))
        return result
    else:
        print('Solution only works if rx has 1 parent which is a Conjunction type')
        return NotImplemented


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
