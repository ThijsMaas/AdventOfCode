import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def solve(ax, ay, bx, by, px, py):
    # Solving linear equation, got a refresher from chatgpt..
    b = ((px * ay) - (py * ax)) / ((bx * ay) - (by * ax))
    if float(b).is_integer():
        a = (py - (by * b)) / ay
        if float(a).is_integer():
            return a, b
    return None, None


@timing
def part1(input_data: str):
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    tokens = 0
    for match in re.finditer(pattern, input_data):
        ax, ay, bx, by, px, py = map(int, match.groups())
        a, b = solve(ax, ay, bx, by, px, py)
        if a and b:
            tokens += int(a * 3 + b)
    return tokens


@timing
def part2(input_data: str):
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    tokens = 0
    prize_offset = 10000000000000
    for match in re.finditer(pattern, input_data):
        ax, ay, bx, by, px, py = map(int, match.groups())
        a, b = solve(ax, ay, bx, by, px + prize_offset, py + prize_offset)
        if a and b:
            tokens += int(a * 3 + b)
    return tokens


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
