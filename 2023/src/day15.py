#!/usr/bin/env python3

from collections import defaultdict


EXAMPLE_INPUT = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


def get_hash(input_text: str):
    value = 0
    for char in input_text:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def part_1(input_text: str):
    print("Part 1")
    input_sequence = input_text.strip().split(",")
    print(sum(get_hash(x) for x in input_sequence))


def part_2(input_text: str):
    print("Part 2")
    input_sequence = input_text.strip().split(",")
    boxes = defaultdict(list)
    for seq in input_sequence:
        if "=" in seq:
            label, focal_length = seq.split("=")
            box = boxes[get_hash(label)]
            for lens in box:
                if lens[0] == label:
                    lens[1] = int(focal_length)
                    break
            else:
                box.append([label, int(focal_length)])
        else:
            label = seq[:-1]
            box = boxes[get_hash(label)]
            for lens in box:
                if lens[0] == label:
                    box.remove(lens)
                    break

    # Calculate
    total = 0
    for box, lenses in boxes.items():
        if not lenses:
            continue
        for i, lens in enumerate(lenses):
            total += (box + 1) * (i + 1) * lens[1]
    print(total)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
