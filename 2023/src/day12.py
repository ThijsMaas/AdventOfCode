#!/usr/bin/env python3

from functools import cache
import re


@cache
def arrangements_from_pattern(search_string: str, *patterns: re.Pattern):
    if len(patterns) == 0:
        # All patterns are exhausted, if there are no more # in the search string, we have a match
        return 0 if "#" in search_string else 1

    matches = 0
    index = 0

    while True:
        m = patterns[0].search(search_string[index:])
        if m is None:
            # No match, this path is a dead end
            break
        if "#" not in search_string[: index + m.start()]:
            # This match is valid, branch of this path
            search_string_remainder = search_string[index + m.end() - 1 :]
            matches += arrangements_from_pattern(search_string_remainder, *patterns[1:])

        # Continue searching for matches
        index += m.start() + 1

    return matches


def part_1(input_text: str):
    print("Part 1")
    total = 0
    for line in input_text.split("\n"):
        search_string, groups_string = line.split(" ")
        group_patterns = [re.compile(f"[.?][#?]{{{int(s)}}}[.?]") for s in groups_string.split(",")]

        arrangements = arrangements_from_pattern(f".{search_string}.", *group_patterns)
        print(arrangements)
        total += arrangements
    print(total)


def part_2(input_text: str):
    print("Part 2")
    total = 0
    for line in input_text.split("\n"):
        search_string, groups_string = line.split(" ")
        # Unfold 5 times
        search_string = "?".join([search_string] * 5)
        groups_string = ",".join([groups_string] * 5)
        group_patterns = [re.compile(f"[.?][#?]{{{int(s)}}}[.?]") for s in groups_string.split(",")]

        arrangements = arrangements_from_pattern(f".{search_string}.", *group_patterns)
        # print(arrangements)
        total += arrangements
    print(total)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
