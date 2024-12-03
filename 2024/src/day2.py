from itertools import pairwise
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing
from operator import lt, gt

EXAMPLE_INPUT = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def check_order(numbers):
    op = lt if numbers[0] < numbers[1] else gt
    for a, b in pairwise(numbers):
        if not (op(a, b) and abs(a - b) <= 3):
            return False
    return True


@timing
def part1(input_data: str):
    safe = 0
    for line in input_data.splitlines():
        numbers = list(map(int, line.split()))
        if check_order(numbers):
            safe += 1
    return safe


def brute_force(numbers):
    if check_order(numbers):
        return True
    else:
        for i in range(len(numbers)):
            # Remove i from numbers and check again
            res = check_order(numbers[:i] + numbers[i + 1 :])
            if res:
                return True
    return False


@timing
def part2(input_data: str):
    safe = 0
    for line in input_data.splitlines():
        numbers = list(map(int, line.split()))
        if brute_force(numbers):
            safe += 1
    return safe


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
