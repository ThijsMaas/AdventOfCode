from dataclasses import dataclass, field
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


@dataclass
class GridMap:
    grid: list[str]
    bounds: tuple[int, int] = field(init=False)

    def __post_init__(self):
        self.bounds = len(self.grid), len(self.grid[0])

    def get(self, i: int, j: int, default=None):
        if 0 <= i < self.bounds[0] and 0 <= j < self.bounds[1]:
            return self.grid[i][j]
        return default

    def first(self, value: str):
        for i, row in enumerate(self.grid):
            for j, char in enumerate(row):
                if char == value:
                    return i, j


def get_visited(gridmap: GridMap, guard: tuple[int, int], curr_dir: tuple[int, int]):
    visited = set([guard])

    while True:
        next_pos = guard[0] + curr_dir[0], guard[1] + curr_dir[1]
        char = gridmap.get(*next_pos)
        if char is None:
            # Out of bounds
            return visited
        elif char == "#":
            # Turn 90 degrees
            curr_dir = NEXT_DIRECTION[curr_dir]
        else:
            # Move in this direction
            guard = next_pos
            visited.add(guard)


@timing
def part1(input_data: str):
    gridmap = GridMap(input_data.splitlines())
    guard = gridmap.first("^")
    visited = get_visited(gridmap, guard, (-1, 0))

    return len(visited)


def is_cycle(gridmap: GridMap, position, curr_dir, new_obstacle, visited: set):
    while True:
        next_pos = position[0] + curr_dir[0], position[1] + curr_dir[1]
        char = gridmap.get(*next_pos)
        if char is None:
            # Found the edge
            return False
        elif char == "#" or next_pos == new_obstacle:
            # Turn 90 degrees
            curr_dir = NEXT_DIRECTION[curr_dir]
        else:
            if (next_pos, curr_dir) in visited:
                # We are in a cycle
                return True
            # Add visited and direction of hit
            visited.add((next_pos, curr_dir))
            # Move in this direction
            position = next_pos


@timing
def part2(input_data: str):
    gridmap = GridMap(input_data.splitlines())
    position = gridmap.first("^")
    new_obstacles = 0

    curr_dir = (-1, 0)
    visited = set([(position, curr_dir)])
    visited_positions = set([position])

    while True:
        next_pos = position[0] + curr_dir[0], position[1] + curr_dir[1]
        char = gridmap.get(*next_pos)
        if char is None:
            # Out of bounds
            break
        elif char == "#":
            # Turn 90 degrees
            curr_dir = NEXT_DIRECTION[curr_dir]
        else:
            # Check if putting a new obstacle in this position starts a cycle after continuing this path
            if next_pos not in visited_positions and is_cycle(gridmap, position, curr_dir, next_pos, visited.copy()):
                new_obstacles += 1

            # Move in this direction
            position = next_pos
            visited.add((position, curr_dir))
            visited_positions.add(position)

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
