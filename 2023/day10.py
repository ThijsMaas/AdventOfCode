from dataclasses import dataclass
from io import TextIOWrapper

import tqdm

Node = tuple[int, int]

Graph = dict[Node, tuple[Node, Node]]


def build_graph(input: TextIOWrapper) -> tuple[Graph, Node]:
    nodes: Graph = {}
    start: Node = (0, 0)

    for y, line in enumerate(input.readlines()):
        for x, char in enumerate(line.strip()):
            if char == ".":
                continue
            if char == "-":
                nodes[(x, y)] = ((x - 1, y), (x + 1, y))
            elif char == "|":
                nodes[(x, y)] = ((x, y - 1), (x, y + 1))
            elif char == "J":
                nodes[(x, y)] = ((x, y - 1), (x - 1, y))
            elif char == "L":
                nodes[(x, y)] = ((x, y - 1), (x + 1, y))
            elif char == "F":
                nodes[(x, y)] = ((x, y + 1), (x + 1, y))
            elif char == "7":
                nodes[(x, y)] = ((x, y + 1), (x - 1, y))
            elif char == "S":
                start = (x, y)
            else:
                raise ValueError(f"Invalid character: {char}")

    # Add the start node
    connecting_nodes = []
    for node in nodes:
        if start in nodes[node]:
            connecting_nodes.append(node)
    nodes[start] = connecting_nodes

    return nodes, start


def find_circular_path(graph: Graph, start: Node) -> list[Node]:
    path = [start]
    previous_node = start
    current_node = graph[start][0]
    while current_node != start:
        if current_node not in graph:
            raise ValueError(f"Invalid node: {current_node}")

        next_node = graph[current_node][0] if graph[current_node][0] != previous_node else graph[current_node][1]
        path.append(current_node)
        previous_node = current_node
        current_node = next_node

    return path


def part_1(input: TextIOWrapper):
    print("Part 1")
    graph, start = build_graph(input)
    path = find_circular_path(graph, start)
    print(len(path) / 2)


def is_inside_path(path: list[Node], position: Node) -> bool:
    if position in path:
        return False

    x, y = position
    n = len(path)
    # Determine with ray casting algorithm
    inside = False
    p1x, p1y = path[0]
    for i in range(n + 1):
        p2x, p2y = path[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def part_2(input: TextIOWrapper):
    print("Part 2")

    graph, start = build_graph(input)

    path = find_circular_path(graph, start)

    # For each position in the path matrix, check if it is within the path area
    height = max(node[1] for node in graph.keys()) - 1
    min_height = min(node[1] for node in graph.keys()) + 1
    width = max(node[0] for node in graph.keys()) - 1
    min_width = min(node[0] for node in graph.keys()) + 1

    inside_positions = []
    for x in tqdm.tqdm(range(min_width, width)):
        for y in range(min_height, height):
            if is_inside_path(path, (x, y)):
                inside_positions.append((x, y))
    print(len(inside_positions))


def solution(input: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input)
    elif part_number == 2:
        part_2(input)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
