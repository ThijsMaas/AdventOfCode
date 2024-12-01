from bisect import insort
from collections import defaultdict
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


@timing
def part1(input_data: str):
    sorted_list1 = []
    sorted_list2 = []
    for line in input_data.splitlines():
        a, b = map(int, line.split())
        insort(sorted_list1, a)
        insort(sorted_list2, b)

    return sum(abs(a - b) for a, b in zip(sorted_list1, sorted_list2))


def part2(input_data: str):
    numbers, counter = [], defaultdict(int)
    for line in input_data.splitlines():
        a, b = map(int, line.split())
        numbers.append(a)
        counter[b] += 1
    score = sum(counter.get(n, 0) * n for n in numbers)
    return score


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
