#!/usr/bin/env python3

DIGIT_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def part_1(input_text: str):
    print("Part 1")
    sum_output = 0
    for line in input_text.split("\n"):
        digit_str = ""
        for char in line:
            if char.isdigit():
                digit_str += char
                break
        for char in line[::-1]:
            if char.isdigit():
                digit_str += char
                break
        sum_output += int(digit_str)
    print(sum_output)


def part_2(input_text: str):
    print("Part 2")
    sum_output = 0
    for line in input_text.split("\n"):
        digit_positions: dict[int, str] = {}
        for i, char in enumerate(line):
            if char.isdigit():
                digit_positions[i] = char
        for digit, word in enumerate(DIGIT_WORDS):
            if word in line:
                digit_positions[line.rfind(word)] = str(digit)
                digit_positions[line.find(word)] = str(digit)
        first, last = (
            digit_positions[min(digit_positions)],
            digit_positions[max(digit_positions)],
        )
        digit_str = first + last
        sum_output += int(digit_str)
    print(sum_output)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
