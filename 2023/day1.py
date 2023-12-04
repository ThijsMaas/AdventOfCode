from io import TextIOWrapper

DIGIT_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part_1(input_file: TextIOWrapper):
    print("Part 1")
    sum_output = 0
    for line in input_file.readlines():
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


def part_2(input_file: TextIOWrapper):
    print("Part 2")
    sum_output = 0
    for line in input_file.readlines():
        digit_positions: dict[int, str] = {}
        for i, char in enumerate(line):
            if char.isdigit():
                digit_positions[i] = char
        for word, digit in DIGIT_WORDS.items():
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


def solution(input_file: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input_file)
    elif part_number == 2:
        part_2(input_file)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
