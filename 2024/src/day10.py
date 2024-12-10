from dataclasses import dataclass, field
import re
from sys import argv

from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


@dataclass
class GridMap:
    grid: list[list[int]]
    bounds: tuple[int, int] = field(init=False)

    def __post_init__(self):
        self.bounds = len(self.grid), len(self.grid[0])

    def _in_bounds(self, i: int, j: int):
        return 0 <= i < self.bounds[0] and 0 <= j < self.bounds[1]

    def get_value(self, i: int, j: int, default=None):
        if self._in_bounds(i, j):
            return self.grid[i][j]
        return default

    def get_positions(self, value: int):
        for i, row in enumerate(self.grid):
            for j, char in enumerate(row):
                if char == value:
                    yield i, j

    def get_neighbors(self, i: int, j: int):
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            neighbor_pos = i + di, j + dj
            if self._in_bounds(*neighbor_pos):
                yield neighbor_pos


@timing
def part1(input_data: str):
    grid = [[int(c) for c in row] for row in input_data.splitlines()]
    gridmap = GridMap(grid)
    starts = [p for p in gridmap.get_positions(0)]
    ends = [p for p in gridmap.get_positions(9)]

    # find all paths from start to ends using bfs
    answer = 0
    for start in starts:
        visited = set()
        queue = [start]
        reachable_end_nodes = set()

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)

            if node in ends:
                reachable_end_nodes.add(node)

            for neighbor in gridmap.get_neighbors(*node):
                if gridmap.get_value(*node) == gridmap.get_value(*neighbor) - 1:
                    if neighbor not in visited:
                        queue.append(neighbor)

        answer += len(reachable_end_nodes)
    return answer


@timing
def part2(input_data: str):
    grid = [[int(c) for c in row] for row in input_data.splitlines()]
    gridmap = GridMap(grid)
    starts = [p for p in gridmap.get_positions(0)]
    ends = set(p for p in gridmap.get_positions(9))

    answer = 0

    def dfs(node, start, visited: set[int]):
        nonlocal answer
        if node in ends:
            answer += 1  # Found a valid path to an end node

        for neighbor in gridmap.get_neighbors(*node):
            if gridmap.get_value(*node) == gridmap.get_value(*neighbor) - 1:
                if neighbor not in visited:
                    # Visit the neighbor
                    visited.add(neighbor)
                    dfs(neighbor, start, visited)
                    visited.remove(neighbor)  # Backtrack

    for start in starts:
        visited = set([start])
        dfs(start, start, visited)

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
