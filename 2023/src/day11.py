#!/usr/bin/env python3

from itertools import combinations


def get_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_galaxies(input_text: str, expansion_rate=1) -> list[tuple[int, int]]:
    galaxies = []
    lines = input_text.split("\n")
    x_len = len(lines[0].strip())
    y_len = len(lines)

    expand_x = list(range(x_len))
    expand_y = list(range(y_len))

    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == "#":
                galaxies.append((x, y))
                if x in expand_x:
                    expand_x.remove(x)
                if y in expand_y:
                    expand_y.remove(y)

    # Expand the galaxies
    expanded_galaxies = []
    for galaxy in galaxies:
        nx_expand = len([x for x in expand_x if x < galaxy[0]]) * expansion_rate
        ny_expand = len([y for y in expand_y if y < galaxy[1]]) * expansion_rate
        expanded_galaxies.append((galaxy[0] + nx_expand, galaxy[1] + ny_expand))

    return expanded_galaxies


def part_1(input_text: str):
    print("Part 1")
    galaxies = get_galaxies(input_text)

    total_distance = sum(get_distance(g1, g2) for g1, g2 in combinations(galaxies, 2))
    print(total_distance)


def part_2(input_text: str):
    print("Part 2")
    expansion_rate = int(1e6)
    galaxies = get_galaxies(input_text, expansion_rate - 1)
    print(f"Galaxies: {len(galaxies)}")

    total_distance = sum(get_distance(g1, g2) for g1, g2 in combinations(galaxies, 2))
    print(f"Total distance: {int(total_distance)}")


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
