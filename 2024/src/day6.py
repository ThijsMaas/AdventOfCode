from itertools import cycle
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

NEXT_DIRECTION = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}


def get_visited(grid_map, guard, curr_dir):
    visited = set([guard])

    while True:
        next_pos = guard[0] + curr_dir[0], guard[1] + curr_dir[1]
        if grid_map.get(next_pos) is None:
            # Found the edge
            break
        elif grid_map[next_pos] == "#":
            # Turn 90 degrees
            curr_dir = NEXT_DIRECTION[curr_dir]
        else:
            # Move in this direction
            guard = next_pos
            visited.add(guard)
    return visited


@timing
def part1(input_data: str):
    grid_map = {(i, j): char for i, row in enumerate(input_data.splitlines()) for j, char in enumerate(row)}
    guard = [k for k, v in grid_map.items() if v == "^"][0]
    start_direction = (-1, 0)
    visited = get_visited(grid_map, guard, start_direction)

    return len(visited)


def check_cycle(grid_map, guard, curr_dir):
    visited_obstacles = set()
    while True:
        # Check if putting an obstruction at the next position will start a cycle
        next_pos = guard[0] + curr_dir[0], guard[1] + curr_dir[1]
        if grid_map.get(next_pos) is None:
            # Found the edge
            return False
        elif grid_map[next_pos] == "#":
            if (guard, curr_dir) in visited_obstacles:
                # We are in a cycle
                return True
            # Add obstacle and direction of hit
            visited_obstacles.add((guard, curr_dir))
            # Turn 90 degrees
            curr_dir = NEXT_DIRECTION[curr_dir]
        else:
            # Move in this direction
            guard = next_pos


@timing
def part2(input_data: str):
    grid_map = {(i, j): char for i, row in enumerate(input_data.splitlines()) for j, char in enumerate(row)}
    guard = [k for k, v in grid_map.items() if v == "^"][0]
    start_direction = (-1, 0)

    visited = get_visited(grid_map, guard, start_direction)
    visited.remove(guard)

    new_obstacles = 0
    for position in visited:
        grid_map[position] = "#"
        if check_cycle(grid_map, guard, start_direction):
            new_obstacles += 1
        grid_map[position] = "."

    return new_obstacles


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
