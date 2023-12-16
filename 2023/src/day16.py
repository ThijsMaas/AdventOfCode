#!/usr/bin/env python3

EXAMPLE_INPUT = """\
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
"""


class Contraption:
    rows: list[list[str]]
    visited: set
    energized: set

    def __init__(self, input_text: str):
        self.rows = []
        for line in input_text.splitlines():
            self.rows.append(list(line))
        self.visited = set()
        self.energized = set()

    def get_char(self, pos: tuple[int, int]):
        return self.rows[pos[1]][pos[0]]

    def get_next_directions(self, direction: str, mirror: str):
        if mirror == "|":
            if direction in ("left", "right"):
                return ["up", "down"]
            else:
                return [direction]
        elif mirror == "-":
            if direction in ("up", "down"):
                return ["left", "right"]
            else:
                return [direction]
        elif mirror == "/":
            if direction == "up":
                return ["right"]
            elif direction == "right":
                return ["up"]
            elif direction == "down":
                return ["left"]
            elif direction == "left":
                return ["down"]
        elif mirror == "\\":
            if direction == "up":
                return ["left"]
            elif direction == "right":
                return ["down"]
            elif direction == "down":
                return ["right"]
            elif direction == "left":
                return ["up"]

    def get_next_position(self, pos: tuple[int, int], direction: str):
        # Return the first position in the given direction
        # If no position is found, return None
        # If a mirror is found, return the mirror position and the new direction

        if direction == "up":
            if pos[1] == 0:
                return None, None
            next_position = (pos[0], pos[1] - 1)
        elif direction == "right":
            if pos[0] == len(self.rows[0]) - 1:
                return None, None
            next_position = (pos[0] + 1, pos[1])
        elif direction == "down":
            if pos[1] == len(self.rows) - 1:
                return None, None
            next_position = (pos[0], pos[1] + 1)
        elif direction == "left":
            if pos[0] == 0:
                return None, None
            next_position = (pos[0] - 1, pos[1])
        else:
            raise ValueError(f"Invalid direction: {direction}")

        next_char = self.get_char(next_position)
        next_directions = self.get_next_directions(direction, next_char)
        return next_position, next_directions

    def get_next_mirror_pos(self, pos: tuple[int, int], direction: str):
        # From some position, find the next mirror in the given direction
        # Set each position traveled though as energized, even when no mirror is found in that direction
        # If no mirror is found at all, return None
        while True:
            next_position, next_directions = self.get_next_position(pos, direction)
            if next_position:
                # Valid position on the board
                self.energized.add(next_position)
                if next_directions:
                    # Next position is a mirror
                    return next_position, next_directions
                else:
                    pos = next_position
            else:
                return None, None

    def follow_beam(self, start, direction):
        queue = []

        # Follow beam
        start_mirror, start_directions = self.get_next_mirror_pos(start, direction)
        if not start_mirror:
            return
        for start_direction in start_directions:
            queue.append((start_mirror, start_direction))

        while queue:
            current_mirror, current_direction = queue.pop(0)

            # Get next mirrors
            next_mirror, next_directions = self.get_next_mirror_pos(current_mirror, current_direction)
            if next_mirror:
                for next_direction in next_directions:
                    if (next_mirror, next_direction) not in self.visited:
                        queue.append((next_mirror, next_direction))
            self.visited.add((current_mirror, current_direction))


def part_1(input_text: str):
    print("Part 1")
    contraption = Contraption(input_text)
    contraption.follow_beam((-1, 0), "right")
    print(len(contraption.energized))


def get_energized(input_text: str, start, direction):
    contraption = Contraption(input_text)
    contraption.follow_beam(start, direction)
    n_energized = len(contraption.energized)
    return n_energized


def part_2(input_text: str):
    print("Part 2")
    max_y = len(input_text.splitlines())
    max_x = len(input_text.splitlines()[0])
    max_energized = 0
    for y in range(max_y):
        energized = get_energized(input_text, (-1, y), "right")
        if energized > max_energized:
            max_energized = energized
            print(y, "right", energized)
        energized = get_energized(input_text, (max_x, y), "left")
        if energized > max_energized:
            max_energized = energized
            print(y, "left", energized)
    for x in range(max_x):
        energized = get_energized(input_text, (x, -1), "down")
        if energized > max_energized:
            max_energized = energized
            print(x, "down", energized)
        energized = get_energized(input_text, (x, max_y), "up")
        if energized > max_energized:
            max_energized = energized
            print(x, "up", energized)
    print(max_energized)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
