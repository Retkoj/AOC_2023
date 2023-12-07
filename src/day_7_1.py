from argparse import ArgumentParser
from collections import Counter
from dataclasses import dataclass
from enum import Enum

FILEPATH = '../data/day_7.txt'
TEST_FILEPATH = '../data/day_7_test.txt'


class HandTypes(Enum):
    FIVE_OAK = 6
    FOUR_OAK = 5
    FULL_HOUSE = 4
    THREE_OAK = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


CARD_ORDER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


@dataclass
class Hand:
    raw_hand: str
    hand: list
    bid: int

    @property
    def hand_type(self) -> HandTypes:
        counts = Counter(self.hand)
        if len(counts) == 1:
            return HandTypes.FIVE_OAK
        if 1 in counts.values() and 4 in counts.values():
            return HandTypes.FOUR_OAK
        if 2 in counts.values() and 3 in counts.values():
            return HandTypes.FULL_HOUSE
        if 1 in counts.values() and 3 in counts.values():
            return HandTypes.THREE_OAK
        if list(counts.values()).count(2) == 2:
            return HandTypes.TWO_PAIR
        if list(counts.values()).count(2) == 1 and list(counts.values()).count(1) == 3:
            return HandTypes.ONE_PAIR
        if list(counts.values()).count(1) == 5:
            return HandTypes.HIGH_CARD

    def __lt__(self, other):
        if self.hand_type.value < other.hand_type.value:
            return True
        elif self.hand_type.value > other.hand_type.value:
            return False
        else:
            for i in range(0, 5):
                if CARD_ORDER.index(self.hand[i]) > CARD_ORDER.index(other.hand[i]):
                    return True
                elif CARD_ORDER.index(self.hand[i]) < CARD_ORDER.index(other.hand[i]):
                    return False
        return True


def solve(data):
    hand_list = []
    for line in data:
        cards, bid = line.split(' ')
        hand_list.append(Hand(cards, list(cards), int(bid)))
    print(hand_list)
    hand_list.sort()
    print(hand_list)
    result = sum([(i + 1) * h.bid for i, h in enumerate(hand_list)])
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
