#!/usr/bin/env python3

EXAMPLE_INPUT = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def tilt(rows: list[list[str]]):
    # North is at x = 0
    for y in range(len(rows)):
        last_block = -1
        for x, char in enumerate(rows[y]):
            if char == "#":
                last_block = x
            elif char == "O":
                if x == last_block + 1:
                    last_block += 1
                    continue
                rows[y][last_block + 1] = "O"
                rows[y][x] = "."
                last_block = last_block + 1


def rotate(rows: list[list[str]]):
    # Rotate 90 degrees clockwise
    return [[row[i] for row in rows] for i in range(len(rows[0]))][::-1]


def get_load(rows: list[list[str]]):
    # North is at x = 0
    load = 0
    for y in range(len(rows)):
        for x, char in enumerate(rows[y]):
            if char == "O":
                load += len(rows) - x
    return load


def part_1(input_text: str):
    print("Part 1")
    original = [list(line) for line in input_text.splitlines()]
    # Transpose so north is at x = 0
    north = [[row[i] for row in original] for i in range(len(original[0]))]
    tilt(north)

    print(get_load(north))


def cycle(north: list[list[str]]):
    tilt(north)
    west = rotate(north)
    tilt(west)
    south = rotate(west)
    tilt(south)
    east = rotate(south)
    tilt(east)
    return rotate(east)


def part_2(input_text: str):
    print("Part 2")
    original = [list(line) for line in input_text.splitlines()]
    # Transpose so north is at x = 0
    north = [[row[i] for row in original] for i in range(len(original[0]))]

    hashes = set()
    loop_hashes = set()
    cycles = int(1e9)

    for i in range(cycles):
        north = cycle(north)
        platform_hash = hash(tuple(tuple(row) for row in north))

        if platform_hash in hashes:
            if platform_hash in loop_hashes:
                break
            else:
                loop_hashes.add(platform_hash)
        hashes.add(platform_hash)

    loop_length = len(loop_hashes)
    print(f"Found loop after {i} cycles")
    print(f"Loop length: {loop_length}")
    before_loop = len(hashes) - loop_length
    n_loops = (cycles - before_loop) // loop_length
    new_cycles = cycles - (n_loops * loop_length)

    print(f"Before loop: {before_loop}")
    print(f"Loops: {n_loops}")
    print(f"New cycles: {new_cycles}")

    north = [[row[i] for row in original] for i in range(len(original[0]))]
    for _ in range(new_cycles):
        north = cycle(north)

    print(get_load(north))


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
