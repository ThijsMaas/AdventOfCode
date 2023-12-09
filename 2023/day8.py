import math
from io import TextIOWrapper
from itertools import cycle


def parse_input(input: TextIOWrapper):
    nodes: dict[str, list[str]] = {}
    directions = cycle(list(input.readline().strip()))
    input.readline()

    for line in input.readlines():
        start = line[:3]
        left = line[7:10]
        right = line[12:15]
        nodes[start] = [left, right]

    return nodes, directions


def part_1(input: TextIOWrapper):
    print("Part 1")
    nodes, directions = parse_input(input)

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


def part_2(input: TextIOWrapper):
    print("Part 2")
    nodes, directions = parse_input(input)

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


def solution(input: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input)
    elif part_number == 2:
        part_2(input)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
