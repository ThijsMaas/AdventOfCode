#!/usr/bin/env python3


def get_differences(numbers: list[int]):
    differences = []
    for i in range(1, len(numbers)):
        differences.append(numbers[i] - numbers[i - 1])
    return differences


def extrapolate(numbers: list[int]):
    difference_lists = [numbers]
    while True:
        differences = get_differences(numbers)
        difference_lists.append(differences)
        if all(d == 0 for d in differences):
            break
        numbers = differences
    # Sum the last value in each list
    return sum([lst[-1] for lst in difference_lists])


def part_1(input_text: str):
    print("Part 1")
    total = 0
    for line in input_text.split("\n"):
        numbers = [int(n) for n in line.split()]
        next_number = extrapolate(numbers)
        total += next_number
    print(total)


def part_2(input_text: str):
    print("Part 2")
    total = 0
    for line in input_text.split("\n"):
        numbers = [int(n) for n in line.split()]
        next_number = extrapolate(numbers[::-1])
        total += next_number
    print(total)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
