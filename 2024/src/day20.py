from collections import defaultdict
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


@timing
def part1(input_data: str):
    nodes = []
    for i, row in enumerate(input_data.splitlines()):
        for j, c in enumerate(row):
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
            if c != "#":
                nodes.append((i, j))
    assert start and end

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # get path from start to end
    queue = [start]
    visited = {start}
    parent = {start: None}
    while queue:
        current = queue.pop(0)
        if current == end:
            break
        for dx, dy in directions:
            wall = (current[0] + dx, current[1] + dy)
            if wall in nodes and wall not in visited:
                queue.append(wall)
                visited.add(wall)
                parent[wall] = current
    path = []
    while current:
        path.append(current)
        current = parent[current]
    path = path[::-1]

    cheats = 0
    for distance, node in enumerate(path):
        # Check if we can cheat from this node to a node further down the path
        for dx, dy in directions:
            wall = (node[0] + dx, node[1] + dy)
            if wall not in nodes:  # We are cheating
                cheat_node = (wall[0] + dx, wall[1] + dy)
                if cheat_node in nodes:
                    # We can cheat from node to new2
                    if cheat_node in path[:distance]:
                        # Wrong direction
                        continue
                    cheat_distance = path.index(cheat_node) - distance - 2
                    if cheat_distance >= 100:
                        cheats += 1
                        # print(f"Cheating from {node} to {cheat_node} with distance {cheat_distance}")
    return cheats


@timing
def part2(input_data: str):
    pass


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
