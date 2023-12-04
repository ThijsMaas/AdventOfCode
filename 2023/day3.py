from io import TextIOWrapper
from typing import NamedTuple
import re


class Number(NamedTuple):
    value: int
    line: int
    start: int
    end: int


class Symbol(NamedTuple):
    value: str
    line: int
    position: int


def is_adjacent(number: Number, symbol: Symbol):
    """Checks if the number and symbol are horizontally, vertically or diagonally adjacent."""
    if number.line == symbol.line:
        # Horizontal
        return number.end == symbol.position - 1 or number.start == symbol.position + 1
    elif number.line == symbol.line - 1 or number.line == symbol.line + 1:
        # Vertical or diagonal
        return symbol.position in range(number.start - 1, number.end + 2)
    else:
        return False


def has_adjacent(number: Number, symbols: list[Symbol]):
    """Checks if the number has any adjacent symbols."""
    for symbol in symbols:
        if is_adjacent(number, symbol):
            return True
    return False


def parse_numbers_and_symbols(
    input_file: TextIOWrapper,
) -> tuple[list[Number], list[Symbol]]:
    """Parses the input file and returns a list of numbers and symbols."""
    number_pattern = r"\d+"
    symbol_pattern = r"[^\d.\n]"
    numbers = []
    symbols = []
    for line_idx, line in enumerate(input_file):
        for digit in re.finditer(number_pattern, line):
            numbers.append(Number(int(digit.group()), line_idx, digit.start(), digit.end() - 1))
        for symbol in re.finditer(symbol_pattern, line):
            symbols.append(Symbol(symbol.group(), line_idx, symbol.start()))
    return numbers, symbols


def part_1(input_file: TextIOWrapper):
    print("Part 1")

    numbers, symbols = parse_numbers_and_symbols(input_file)

    # Finding adjacent numbers
    part_numbers = []
    for number in numbers:
        if has_adjacent(number, symbols):
            part_numbers.append(number.value)

    print(f"Part number sum: {sum(part_numbers)}")


def is_gear(symbol: Symbol, numbers: list[Number]):
    adjacent_numbers: list[Number] = []
    for number in numbers:
        if is_adjacent(number, symbol):
            adjacent_numbers.append(number)
    if len(adjacent_numbers) == 2:
        return adjacent_numbers[0].value * adjacent_numbers[1].value
    return None


def part_2(input_file: TextIOWrapper):
    print("Part 2")
    gear_sum = 0
    numbers, symbols = parse_numbers_and_symbols(input_file)
    for symbol in symbols:
        if gear := is_gear(symbol, numbers):
            gear_sum += gear

    print(f"Gear sum: {gear_sum}")


def solution(input_file: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input_file)
    elif part_number == 2:
        part_2(input_file)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
