#!/usr/bin/env python3

EXAMPLE_INPUT = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


def generate_polygon(input_text: str):
    polygon = [(0, 0)]
    circumference = 0
    for line in input_text.splitlines():
        direction, length = line.split()[:2]
        circumference += int(length)
        previous = polygon[-1]
        if direction == "R":
            polygon.append((previous[0] + int(length), previous[1]))
        elif direction == "U":
            polygon.append((previous[0], previous[1] - int(length)))
        elif direction == "L":
            polygon.append((previous[0] - int(length), previous[1]))
        elif direction == "D":
            polygon.append((previous[0], previous[1] + int(length)))
        else:
            raise ValueError(f"Invalid direction: {direction}")

    return polygon[:-1], circumference


def generate_polygon_2(input_text: str):
    polygon = [(0, 0)]
    circumference = 0
    for line in input_text.splitlines():
        code = line.split(" ")[2][2:-1]
        length = int(code[:5], 16)
        direction = code[5]

        circumference += int(length)
        previous = polygon[-1]
        if direction == "0":
            polygon.append((previous[0] + int(length), previous[1]))
        elif direction == "3":
            polygon.append((previous[0], previous[1] - int(length)))
        elif direction == "2":
            polygon.append((previous[0] - int(length), previous[1]))
        elif direction == "1":
            polygon.append((previous[0], previous[1] + int(length)))
        else:
            raise ValueError(f"Invalid direction: {direction}")

    return polygon[:-1], circumference


def shoelace_area(polygon):
    x_cords, y_cords = zip(*polygon)
    return abs(sum(x_cords[i - 1] * y_cords[i] - x_cords[i] * y_cords[i - 1] for i in range(len(x_cords)))) / 2


def part_1(input_text: str):
    print("Part 1")
    polygon, circumference = generate_polygon(input_text)
    print(int(shoelace_area(polygon) + (circumference / 2) + 1))


def part_2(input_text: str):
    print("Part 2")

    polygon, circumference = generate_polygon_2(input_text)
    print(int(shoelace_area(polygon) + (circumference / 2) + 1))


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
