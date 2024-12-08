from collections import defaultdict
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def get_anti_nodes(a: tuple[int, int], b: tuple[int, int], bounds: tuple[int, int], limit=1):
    a_x, a_y, b_x, b_y = *a, *b
    diff_x, diff_y = a_x - b_x, a_y - b_y
    a = 1
    while a <= limit:
        anti_a = a_x + a * diff_x, a_y + a * diff_y
        if is_in_bounds(anti_a, *bounds):
            yield anti_a
        else:
            break
        a += 1

    b = 1
    while b <= limit:
        anti_b = b_x - b * diff_x, b_y - b * diff_y
        if is_in_bounds(anti_b, *bounds):
            yield anti_b
        else:
            break
        b += 1


def is_in_bounds(node: tuple[int, int], height: int, width: int):
    return 0 <= node[0] <= height and 0 <= node[1] <= width


@timing
def part1(input_data: str):
    antennas = defaultdict(list)
    for i, row in enumerate(input_data.splitlines()):
        for j, char in enumerate(row):
            if char != ".":
                antennas[char].append((i, j))
    height, width = i, j

    anti_nodes = set()
    for group in antennas.values():
        # Compare every antenna in a group to each other
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                for anti_node in get_anti_nodes(a, b, (height, width), 1):
                    if is_in_bounds(anti_node, height, width):
                        anti_nodes.add(anti_node)

    return len(anti_nodes)


@timing
def part2(input_data: str):
    antennas = defaultdict(list)
    for i, row in enumerate(input_data.splitlines()):
        for j, char in enumerate(row):
            if char != ".":
                antennas[char].append((i, j))
    height, width = i, j

    anti_nodes = set()
    for group in antennas.values():
        # Compare every antenna in a group to each other
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                for anti_node in get_anti_nodes(a, b, (height, width), 999):
                    if is_in_bounds(anti_node, height, width):
                        anti_nodes.add(anti_node)

    # add all the antennas
    anti_nodes = anti_nodes | set(a for group in antennas.values() for a in group)
    return len(anti_nodes)


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
