Boilerplate for each day:

```python
from io import TextIOWrapper


def part_1(input: TextIOWrapper):
    print("Part 1")

def part_2(input: TextIOWrapper):
    print("Part 2")


def solution(input: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input)
    elif part_number == 2:
        part_2(input)
    else:
        raise ValueError(f"Invalid part number: {part_number}")

```