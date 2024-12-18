from collections import deque
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def print_coords(coords, size, path):
    for y in range(size + 1):
        row = ""
        for x in range(size + 1):
            if (x, y) in coords:
                row += "#"
            elif (x, y) in path:
                row += "O"
            else:
                row += "."

        print(row)


def bfs(corrupted, size, start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            ni, nj = current[0] + di, current[1] + dj
            # if out of bounds, or corrupted
            if 0 <= ni < size and 0 <= nj < size and (ni, nj) not in corrupted:
                if (ni, nj) not in visited:
                    visited.add((ni, nj))
                    parent[(ni, nj)] = current
                    queue.append((ni, nj))

    return None


@timing
def part1(input_data: str):
    coords = [eval(b) for b in input_data.splitlines()]
    size = 70
    count = 1024

    path = bfs(coords[:count], size + 1, (0, 0), (size, size))
    return len(path) - 1


@timing
def part2(input_data: str):
    coords = [eval(b) for b in input_data.splitlines()]
    size = 70  # Example: 6
    previous_path = None
    for i in range(1, len(coords)):
        if previous_path and coords[i - 1] not in previous_path:
            continue
        print(i, coords[i - 1])
        path = bfs(coords[:i], size + 1, (0, 0), (size, size))
        if not path:
            break
        # print_coords(coords[:i], size, path)
        previous_path = path
    byte = coords[i - 1]
    return f"{byte[0]},{byte[1]}"


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
