from collections import defaultdict
from dataclasses import dataclass
from functools import cache
import math
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
125 17
"""


@dataclass
class Stones:
    stones: dict[int, int]

    def blink(self):
        new_stones = defaultdict(int)
        for stone, count in self.stones.items():
            if stone == 0:
                new_stones[1] += count
            elif even_digits(stone):
                a, b = split_stone(stone)
                new_stones[a] += count
                new_stones[b] += count
            else:
                new_stones[stone * 2024] += count
        self.stones = new_stones

    def __len__(self):
        return sum(self.stones.values())


@cache
def even_digits(value):
    # Assumes value is never 0
    return math.floor(math.log10(value)) % 2 == 1


@cache
def split_stone(value) -> tuple[int, int]:
    half_power = 10 ** (len(str(value)) // 2)
    return divmod(value, half_power)


@timing
def part1(input_data: str):
    stone_counter = defaultdict(int)
    for stone in input_data.strip().split():
        stone_counter[int(stone)] += 1
    stones = Stones(stone_counter)

    blinks = 25
    for _ in range(blinks):
        # print(stones)
        stones.blink()

    return len(stones)


@timing
def part2(input_data: str):
    stone_counter = defaultdict(int)
    for stone in input_data.strip().split():
        stone_counter[int(stone)] += 1
    stones = Stones(stone_counter)

    blinks = 75
    for _ in range(blinks):
        # print(stones)
        stones.blink()

    return len(stones)


if __name__ == "__main__":
    """Main script to run the solutions, use flag 'e' for the example input and 's' to submit"""
    year, day = list(map(int, re.search(r"(\d{4})/src/day(\d+).py", __file__).groups()))

    # Get input data
    if len(argv) == 2 and argv[1] == "e":
        input_data = EXAMPLE_INPUT
    else:
        input_data = get_input(year, day)

    # Get answers and submit
    answer1 = part1(input_data)
    print(f"Answer part 1: {answer1}")
    if len(argv) == 2 and argv[1] == "s" and answer1 is not None:
        assert submit_answer(year, day, 1, answer1)

    answer2 = part2(input_data)
    print(f"Answer part 2: {answer2}")
    if len(argv) == 2 and argv[1] == "s" and answer2 is not None:
        assert submit_answer(year, day, 2, answer2)
