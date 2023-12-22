#!/usr/bin/env python3

from copy import deepcopy
from dataclasses import dataclass
from functools import cache


EXAMPLE_INPUT = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


@dataclass
class Brick:
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def get_x_y_cords(self):
        for x in range(self.x[0], self.x[1] + 1):
            for y in range(self.y[0], self.y[1] + 1):
                yield (x, y)

    def __contains__(self, cord: tuple[int, int, int]):
        x, y, z = cord
        return self.x[0] <= x <= self.x[1] and self.y[0] <= y <= self.y[1] and self.z[0] <= z <= self.z[1]


def parse_input(input_text: str) -> list[Brick]:
    bricks = []
    for line in input_text.splitlines():
        start, end = line.strip().split("~")
        start_x, start_y, start_z = list(map(int, start.split(",")))
        end_x, end_y, end_z = list(map(int, end.split(",")))
        min_x, max_x = min(start_x, end_x), max(start_x, end_x)
        min_y, max_y = min(start_y, end_y), max(start_y, end_y)
        min_z, max_z = min(start_z, end_z), max(start_z, end_z)
        brick = Brick((min_x, max_x), (min_y, max_y), (min_z, max_z))
        bricks.append(brick)
    return bricks


def drop_bricks(bricks: list[Brick]):
    # Sort on z start value, so we can iterate from the bottom up
    bricks.sort(key=lambda brick: brick.z[0])

    x_max = max(brick.x[1] for brick in bricks)
    y_max = max(brick.y[1] for brick in bricks)

    # Store a z height map for each x, y coordinate
    z_map = [[0] * (x_max + 1) for _ in range(y_max + 1)]
    for brick in bricks:
        # Find the highest z value for each x, y coordinate
        new_z = max(z_map[y][x] for x, y in brick.get_x_y_cords()) + 1
        # Update the brick and z height map
        brick.z = (new_z, new_z + brick.z[1] - brick.z[0])
        for x, y in brick.get_x_y_cords():
            z_map[y][x] = brick.z[1]


def get_support_graph(bricks: list[Brick]) -> dict[Brick, tuple[set[Brick], set[Brick]]]:
    # For each brick, find the number of bricks it supports and the number of bricks it is supported by
    graph: dict[Brick, tuple[set[Brick], set[Brick]]] = {}
    for brick in bricks:
        graph[brick] = (set(), set())
        for x, y in brick.get_x_y_cords():
            cord_above = (x, y, brick.z[1] + 1)
            cord_below = (x, y, brick.z[0] - 1)
            for other in bricks:
                if other is brick:
                    continue
                if cord_above in other:
                    graph[brick][1].add(other)
                if cord_below in other:
                    graph[brick][0].add(other)
    return graph


def part_1(input_text: str):
    print("Part 1")
    bricks = parse_input(input_text)
    print(f"Number of bricks: {len(bricks)}")
    drop_bricks(bricks)

    brick_support_graph = get_support_graph(bricks)

    n_disintegrate = 0
    for brick in bricks:
        # If all bricks above are supported by multiple bricks, this brick can disintegrate
        if all(len(brick_support_graph[other][0]) > 1 for other in brick_support_graph[brick][1]):
            n_disintegrate += 1
    print(n_disintegrate)


def get_chain_reaction(dis_brick: Brick, brick_support_graph: dict[Brick, tuple[set[Brick], set[Brick]]]):
    n_falling = 0
    for brick in brick_support_graph[dis_brick][1]:
        if dis_brick in brick_support_graph[brick][0]:
            brick_support_graph[brick][0].remove(dis_brick)
        if len(brick_support_graph[brick][0]) == 0:
            n_falling += 1 + get_chain_reaction(brick, brick_support_graph)

    return n_falling


def part_2(input_text: str):
    print("Part 2")
    print("Part 1")
    bricks = parse_input(input_text)
    print(f"Number of bricks: {len(bricks)}")
    drop_bricks(bricks)

    brick_support_graph = get_support_graph(bricks)

    n_sum = 0
    for brick in bricks:
        new_support_graph = deepcopy(brick_support_graph)
        n_falling = get_chain_reaction(brick, new_support_graph)
        n_sum += n_falling
        print(brick, n_falling)
    print(n_sum)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
