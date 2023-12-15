#!/usr/bin/env python3

import math
from itertools import cycle


def parse_input(input_text: str):
    nodes: dict[str, list[str]] = {}
    lines = input_text.split("\n")
    directions = cycle(list(lines[0].strip()))

    for line in lines[2:]:
        start = line[:3]
        left = line[7:10]
        right = line[12:15]
        nodes[start] = [left, right]

    return nodes, directions


def part_1(input_text: str):
    print("Part 1")
    nodes, directions = parse_input(input_text)

    start = "AAA"
    end = "ZZZ"
    steps = 0
    node = nodes[start]

    while True:
        d = next(directions)
        next_node = node[0] if d == "L" else node[1]
        node = nodes[next_node]
        steps += 1

        if next_node == end:
            print("Found end")
            break
    print(steps)


def part_2(input_text: str):
    print("Part 2")
    nodes, directions = parse_input(input_text)

    start_nodes = [node for key, node in nodes.items() if key.endswith("A")]

    loop_end = []
    for node in start_nodes:
        steps = 0
        while True:
            d = next(directions)
            next_node = node[0] if d == "L" else node[1]
            node = nodes[next_node]
            steps += 1
            if next_node.endswith("Z"):
                break
        loop_end.append(steps)
        print(steps)

    # get the least common multiple
    print(math.lcm(*loop_end))


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
