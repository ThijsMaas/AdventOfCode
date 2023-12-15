from importlib import import_module
from sys import argv
import aocd


def touch_day_file():
    boiler_plate = """\
#!/usr/bin/env python3

EXAMPLE_INPUT = \"\"\"\\
?
\"\"\"


def part_1(input_text: str):
    print("Part 1")


def part_2(input_text: str):
    print("Part 2")


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
"""
    day = argv[2]
    with open(f"src/day{day}.py", "w") as f:
        f.write(boiler_plate)


def main():
    if argv[1] == "init":
        touch_day_file()

    day_number = argv[1]
    part_number = int(argv[2]) if len(argv) >= 3 else 1

    use_example = argv[3] == "e" if len(argv) == 4 else False

    for i in range(1, 26):
        if day_number == str(i):
            day_module = import_module(f"src.day{day_number}")
            if use_example:
                input_data = day_module.EXAMPLE_INPUT
            else:
                input_data = aocd.get_data(year=2023, day=i)
            day_module.solution(input_data, part_number)
            break


if __name__ == "__main__":
    main()
