#!/usr/bin/env python3

import itertools
from typing import NamedTuple


EXAMPLE_INPUT = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


class HailStoneXY(NamedTuple):
    px: int
    py: int
    vx: int
    vy: int
    slope: float
    intercept: float


def parse_input(input_text: str):
    for line in input_text.splitlines():
        px, py, _ = map(int, line.split(" @ ")[0].split(", "))
        vx, vy, _ = map(int, line.split(" @ ")[1].split(", "))
        p2x, p2y = px + vx, py + vy
        slope = (py - p2y) / (px - p2x)
        intercept = py - (slope * px)
        yield HailStoneXY(px, py, vx, vy, slope, intercept)


def part_1(input_text: str):
    print("Part 1")

    hailstones = list(parse_input(input_text))

    intersection_min = 200000000000000
    intersection_max = 400000000000000
    intersections = 0

    for stone1, stone2 in itertools.combinations(hailstones, 2):
        if stone1.slope == stone2.slope:
            continue
        intersection_x = (stone1.intercept - stone2.intercept) / (stone2.slope - stone1.slope)
        intersection_y = stone1.slope * intersection_x + stone1.intercept
        if (
            intersection_x < intersection_min
            or intersection_x > intersection_max
            or intersection_y < intersection_min
            or intersection_y > intersection_max
        ):
            continue

        if stone1.vx < 0 and intersection_x > stone1.px:
            continue
        if stone1.vx > 0 and intersection_x < stone1.px:
            continue
        if stone2.vx < 0 and intersection_x > stone2.px:
            continue
        if stone2.vx > 0 and intersection_x < stone2.px:
            continue
        intersections += 1

    print(intersections)


def part_2(input_text: str):
    print("Part 2")


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
