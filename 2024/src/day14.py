from collections import defaultdict
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def future_position(seconds, px, py, vx, vy, sx, sy):
    x = (px + seconds * vx) % sx
    y = (py + seconds * vy) % sy
    return x, y


def print_robots(robots: list, sx, sy, quadrants=False):
    for y in range(sy):
        if quadrants and y == sy // 2:
            print(" " * sx)
            continue
        row = ""
        for x in range(sx):
            if quadrants and x == sx // 2:
                row += " "
                continue

            n = robots.count((x, y))
            row += str(n) if n > 0 else "."
        print(row)


@timing
def part1(input_data: str):
    sx, sy = 101, 103
    seconds = 100
    quadrants = [[0, 0], [0, 0]]
    robots = []
    for line in input_data.splitlines():
        px, py, vx, vy = map(int, re.findall(r"(-?\d+)", line))
        fx, fy = future_position(seconds, px, py, vx, vy, sx, sy)
        robots.append((fx, fy))
        if fx == (sx // 2) or fy == (sy // 2):
            # not in quadrant
            continue
        xq = 0 if fx < sx / 2 else 1
        yq = 0 if fy < sy / 2 else 1
        quadrants[yq][xq] += 1
    return quadrants[0][0] * quadrants[1][0] * quadrants[0][1] * quadrants[1][1]


def longest_vertical_line(robots: list[tuple[int, int]]):
    longest_xy = 0
    y_coords_map = defaultdict(list)
    for x, y, _, _ in robots:
        y_coords_map[x].append(y)

    for x, ys in y_coords_map.items():
        ys.sort()
        longest_y = 1
        current_y = 1
        for i in range(1, len(ys)):
            if ys[i] == ys[i - 1] + 1:
                current_y += 1
            else:
                longest_y = max(longest_y, current_y)
                current_y = 1
        longest_xy = max(longest_xy, longest_y)
    return longest_xy


@timing
def part2(input_data: str):
    sx, sy = 101, 103
    robots: list[tuple[int, int, int, int]] = []
    for line in input_data.splitlines():
        px, py, vx, vy = map(int, re.findall(r"(-?\d+)", line))
        robots.append((px, py, vx, vy))

    for i in range(0, 9999):
        robots = [((px + vx) % sx, (py + vy) % sy, vx, vy) for px, py, vx, vy in robots]

        # Look for n robots lining up vertically?
        n = 10
        if longest_vertical_line(robots) > n:
            print_robots([(px, py) for px, py, _, _ in robots], sx, sy)
            if input("Is this a Christmas Tree? y/n ") == "y":
                break

    return i


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
