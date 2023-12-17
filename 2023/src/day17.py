#!/usr/bin/env python3

from heapq import heappush, heappop
from typing import NamedTuple


EXAMPLE_INPUT = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


class Node(NamedTuple):
    x: int
    y: int


RIGHT = Node(1, 0)
DOWN = Node(0, 1)
LEFT = Node(-1, 0)
UP = Node(0, -1)


class Grid:
    rows: list[list[int]]
    width: int
    height: int

    def __init__(self, input_text: str) -> None:
        self.rows = []
        for line in input_text.splitlines():
            self.rows.append(list(map(int, line)))
        self.width = len(self.rows[0])
        self.height = len(self.rows)

    def get_next_node(self, node: Node, direction: Node):
        new_node = Node(node.x + direction.x, node.y + direction.y)
        if new_node.x < 0 or new_node.y < 0 or new_node.x >= self.width or new_node.y >= self.height:
            return None
        return new_node

    def get_cost(self, node: Node):
        return self.rows[node.y][node.x]

    def find_path(self, end: tuple[int, int], min_consecutive: int, max_consecutive: int):
        visited = set()
        # Initialize the nodes list with the two start directions down (0, 1) and right ( 1, 0)
        nodes = [(0, Node(0, 0), DOWN, 1), (0, Node(0, 0), RIGHT, 1)]

        while len(nodes) > 0:
            cost, node, direction, directions_count = heappop(nodes)
            if (node, direction, directions_count) in visited:
                continue
            visited.add((node, direction, directions_count))
            if new_node := self.get_next_node(node, direction):
                new_cost = cost + self.get_cost(new_node)

                if directions_count >= min_consecutive and directions_count <= max_consecutive:
                    if new_node == end:
                        return new_cost
                for new_direction in [UP, DOWN, LEFT, RIGHT]:
                    if new_direction.y + direction.y == 0 and new_direction.x + direction.x == 0:
                        # Don't go back
                        continue
                    new_direction_count = directions_count + 1 if new_direction == direction else 1
                    if (
                        new_direction != direction and directions_count < min_consecutive
                    ) or new_direction_count > max_consecutive:
                        continue
                    heappush(nodes, (new_cost, new_node, new_direction, new_direction_count))


def part_1(input_text: str):
    print("Part 1")
    grid = Grid(input_text)
    end = (len(grid.rows[0]) - 1, len(grid.rows) - 1)
    cost = grid.find_path(end, 1, 3)
    print(cost)


def part_2(input_text: str):
    print("Part 2")
    grid = Grid(input_text)
    end = (len(grid.rows[0]) - 1, len(grid.rows) - 1)
    cost = grid.find_path(end, 4, 10)
    print(cost)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
