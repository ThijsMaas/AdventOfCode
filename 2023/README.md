# Advent of Code 2023
[Calendar](https://adventofcode.com/2023)

This is the boilerplate I start each day with to make it easy to run from the main script.

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

With this I can simply run the following to get the solution for day 1, part 1 and day 1, part 2.

```bash
python main.py 1 1
python main.py 1 2
```
