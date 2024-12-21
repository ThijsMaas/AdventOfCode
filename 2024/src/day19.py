from functools import cache
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def find_pattern(towels: list[str], design: str):
    @cache
    def recurse(remainder: str):
        if not remainder:
            return True
        return any(recurse(remainder[len(towel) :]) for towel in towels if remainder.startswith(towel))

    return recurse(design)


@timing
def part1(input_data: str):
    str1, str2 = input_data.split("\n\n")
    towels = set(str1.split(", "))
    designs = str2.splitlines()
    return sum(find_pattern(towels, design) for design in designs)


def find_n_patterns(towels: list[str], design: str):
    @cache
    def recurse(remainder: str):
        if not remainder:
            return 1
        return sum(recurse(remainder[len(towel) :]) for towel in towels if remainder.startswith(towel))

    return recurse(design)


@timing
def part2(input_data: str):
    str1, str2 = input_data.split("\n\n")
    towels = set(str1.split(", "))
    designs = str2.splitlines()
    return sum(find_n_patterns(towels, design) for design in designs)


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
