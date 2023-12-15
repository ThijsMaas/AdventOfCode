#!/usr/bin/env python3


def shortest_equal(l1, l2) -> bool:
    for x, y in zip(l1, l2):
        if x != y:
            return False
    return True


def find_mirror_index(lists: list[str]) -> int:
    for i in range(0, len(lists) - 1):
        left_side = lists[i::-1]
        right_side = lists[i + 1 :]
        if shortest_equal(left_side, right_side):
            return i + 1
    return 0


def search_pattern(pattern: str) -> int:
    rows = pattern.split("\n")
    cols = ["".join([row[i] for row in rows]) for i in range(len(rows[0]))]

    # Find the mirror index
    if row_index := find_mirror_index(rows):
        # print(f"Mirror row index: {row_index}")
        return row_index * 100
    elif col_index := find_mirror_index(cols):
        # print(f"Mirror col index: {col_index}")
        return col_index
    else:
        raise ValueError("No mirror index found")


def find_mirror_index_smudge(lists: list[str]) -> int:
    for i in range(0, len(lists) - 1):
        left_side = lists[i::-1]
        right_side = lists[i + 1 :]
        if shortest_equal_smudge(left_side, right_side):
            return i + 1
    return 0


def hamming_distance(s1, s2) -> int:
    return sum([x != y for x, y in zip(s1, s2)])


def shortest_equal_smudge(l1, l2) -> bool:
    n_smudge = 0
    for x, y in zip(l1, l2):
        d = hamming_distance(x, y)
        if d <= 1:
            n_smudge += d
            if n_smudge > 1:
                return False
        else:
            return False
    return n_smudge == 1


def search_pattern_smudge(pattern: str) -> int:
    rows = pattern.split("\n")
    cols = ["".join([row[i] for row in rows]) for i in range(len(rows[0]))]

    # Find the mirror index
    if row_index := find_mirror_index_smudge(rows):
        # print(f"Mirror row index: {row_index}")
        return row_index * 100
    elif col_index := find_mirror_index_smudge(cols):
        # print(f"Mirror col index: {col_index}")
        return col_index
    else:
        raise ValueError("No mirror index found")


def part_1(input_text: str):
    print("Part 1")
    num_sum = 0
    for pattern in input_text.split("\n\n"):
        num = search_pattern(pattern)
        num_sum += num
    print(f"total: {num_sum}")


def part_2(input_text: str):
    print("Part 2")
    num_sum = 0
    for pattern in input_text.split("\n\n"):
        num = search_pattern_smudge(pattern)
        num_sum += num
    print(f"total: {num_sum}")


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
