import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


@timing
def part1(input_data: str):
    grid_map = {(i, j): char for i, row in enumerate(input_data.splitlines()) for j, char in enumerate(row)}

    xmas_paths = []
    for (i, j), char in grid_map.items():
        if char != "X":
            continue
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
            ni, nj = i + di, j + dj
            if grid_map.get((ni, nj)) == "M":
                path = [(i, j), (ni, nj)]
                ni, nj = ni + di, nj + dj
                if grid_map.get((ni, nj)) == "A":
                    path.append((ni, nj))
                    ni, nj = ni + di, nj + dj
                    if grid_map.get((ni, nj)) == "S":
                        path.append((ni, nj))
                        xmas_paths.append(path)

    return len(xmas_paths)


@timing
def part2(input_data: str):
    xmas_paths = []
    grid = input_data.splitlines()

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "A":
                # Check if A is not on the grid edge
                if 1 <= i < len(grid) - 1 and 1 <= j < len(grid[0]) - 1:
                    # Look for X-MAS cross pattern centered on this A
                    if set([grid[i - 1][j - 1], grid[i + 1][j + 1]]) == set(["M", "S"]) and set(
                        [grid[i - 1][j + 1], grid[i + 1][j - 1]]
                    ) == set(["M", "S"]):
                        xmas_paths.append((i, j))
    return len(xmas_paths)


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
