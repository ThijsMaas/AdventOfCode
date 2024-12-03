import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""


@timing
def part1(input_data: str):
    return sum(int(a) * int(b) for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input_data))


@timing
def part2(input_data: str):
    s = 0
    mul = True
    for a, b, do, dont in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", input_data):
        if do:
            mul = True
        elif dont:
            mul = False
        elif mul:
            s += int(a) * int(b)
    return s


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
