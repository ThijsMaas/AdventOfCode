import re
from sys import argv
from api import get_input, submit_answer
from utils import timing
from operator import mul, add

EXAMPLE_INPUT = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def concat(a: int, b: int):
    return a * 10 ** len(str(b)) + b


def solve(answer, numbers, operations, index, test_value):
    if index == len(numbers):
        return answer == test_value
    return any(solve(op(answer, numbers[index]), numbers, operations, index + 1, test_value) for op in operations)


@timing
def part1(input_data: str):
    answer = 0
    for line in input_data.splitlines():
        test_value = int(line.split(":")[0])
        numbers = tuple(map(int, line.split()[1:]))
        operations = [mul, add]
        if solve(numbers[0], numbers, operations, 1, test_value):
            answer += test_value
    return answer


@timing
def part2(input_data: str):
    answer = 0
    for line in input_data.splitlines():
        test_value = int(line.split(":")[0])
        numbers = tuple(map(int, line.split()[1:]))
        operations = [mul, add, concat]
        if solve(numbers[0], numbers, operations, 1, test_value):
            answer += test_value
    return answer


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
