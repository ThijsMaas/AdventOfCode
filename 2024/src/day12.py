from collections import defaultdict
from dataclasses import dataclass, field
from pprint import pprint
import re
from sys import argv

from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


@dataclass
class GridMap:
    grid: list[str]
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


def dfs(node, start, region: set[int], grid: GridMap):
    for neighbor in grid.get_neighbors(*node):
        if grid.get_value(*node) == grid.get_value(*neighbor) and neighbor not in region:
            # Visit the neighbor
            region.add(neighbor)
            dfs(neighbor, start, region, grid)
    return region


def region_boundary(region: list[tuple[int, int]], grid: GridMap):
    boundary = 0
    for i, j in region:
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            neighbor_plant = i + di, j + dj
            if not grid._in_bounds(*neighbor_plant) or grid.get_value(i, j) != grid.get_value(*neighbor_plant):
                # If a position in region has a neighbor that is not of the same plant or is on the edge of the garden,
                # this side of the plant is a region boundary
                boundary += 1
    return boundary


def region_sides(region: list[tuple[int, int]], grid: GridMap):
    boundaries = []
    for i, j in region:
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            neighbor_plant = i + di, j + dj
            if not grid._in_bounds(*neighbor_plant) or grid.get_value(i, j) != grid.get_value(*neighbor_plant):
                # If a position in region has a neighbor that is not of the same plant or is on the edge of the garden,
                # this side of the plant is a region boundary
                boundaries.append(((i, j), (di, dj)))
    to_merge = 0
    for i, (bound1, dir1) in enumerate(boundaries):
        for bound2, dir2 in boundaries[i + 1 :]:
            # check if same direction and side by side
            if dir1 == dir2 and abs(bound1[0] - bound2[0]) + abs(bound1[1] - bound2[1]) == 1:
                to_merge += 1
    return len(boundaries) - to_merge


@timing
def part1(input_data: str):
    grid = GridMap(input_data.splitlines())
    regions = []
    for i, row in enumerate(input_data.splitlines()):
        for j, plant in enumerate(row):
            for region in regions:
                if (i, j) in region:
                    break
            else:
                start = (i, j)
                plant_region = set([start])
                # Do a search through all neighbors of the same plant type to find all plants in this region
                plant_region = dfs(start, start, plant_region, grid)
                regions.append(plant_region)
    return sum(len(r) * region_boundary(r, grid) for r in regions)


@timing
def part2(input_data: str):
    grid = GridMap(input_data.splitlines())
    regions = []
    for i, row in enumerate(input_data.splitlines()):
        for j, plant in enumerate(row):
            for region in regions:
                if (i, j) in region:
                    break
            else:
                # Find region of this plant
                start = (i, j)
                plant_region = set([start])
                plant_region = dfs(start, start, plant_region, grid)
                regions.append(plant_region)
    return sum(len(r) * region_sides(r, grid) for r in regions)


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
