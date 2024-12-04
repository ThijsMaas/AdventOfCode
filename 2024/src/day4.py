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
    xmas_paths = []
    grid = input_data.splitlines()

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "X":
                # Look for a XMAS match in any direction
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
                    ni, nj = i + di, j + dj
                    # Check if valid in grid and matching next char
                    if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] == "M":
                        xmas = [(i, j), (ni, nj)]
                        # Continue search in this direction
                        ni, nj = ni + di, nj + dj
                        # Check if valid in grid and matching next char
                        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] == "A":
                            xmas.append((ni, nj))
                            ni, nj = ni + di, nj + dj
                            # Check if valid in grid and matching next char
                            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] == "S":
                                xmas.append((ni, nj))
                                xmas_paths.append(xmas)
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
