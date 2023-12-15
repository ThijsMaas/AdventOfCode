#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int

    def __gt__(self, other: "Range"):
        return self.start > other.start

    def __iter__(self):
        return iter((self.start, self.end))


@dataclass
class RangeMap(Range):
    diff: int

    def __gt__(self, other: "Range"):
        return self.start > other.start

    def __iter__(self):
        return iter((self.start, self.end, self.diff))


def yield_mapped_ranges(mapping: list[RangeMap], pairs: list[Range]):
    for value in pairs:
        for range_map in mapping:
            yield Range(value.start, min(range_map.start, value.end))
            yield Range(
                max(range_map.start, value.start) + range_map.diff,
                min(range_map.end, value.end) + range_map.diff,
            )
            value.start = max(value.start, min(range_map.end, value.end))
        yield Range(value.start, value.end)


def parse_mappings(mapping_records: list[str]) -> list[list[RangeMap]]:
    mappings: list[list[RangeMap]] = []
    output = "seed"
    for mapping_record in mapping_records:
        input, rest = mapping_record.split("-to-")
        assert input == output
        output, rest = rest.split(" map:\n")
        value_ranges = [
            RangeMap(int(start_input), int(start_input) + int(range_length), int(start_output) - int(start_input))
            for start_output, start_input, range_length in [line.split() for line in rest.split("\n")]
        ]
        value_ranges.sort(key=lambda range_map: range_map.start)

        mappings.append(value_ranges)
    return mappings


def part_1(input_text: str):
    print("Part 1")

    seed_line, *mapping_records = input_text.split("\n\n")
    mappings = parse_mappings(mapping_records)
    seeds_values = [int(seed) for seed in seed_line.split(": ")[1].split()]
    seed_ranges = [
        Range(seed_start, seed_start + 1) for seed_start, seed_length in zip(seeds_values[::2], seeds_values[1::2])
    ]

    values_ranges = seed_ranges
    for mapping in mappings:
        values_ranges = [r for r in yield_mapped_ranges(mapping, values_ranges) if r.start < r.end]

    min_location_value = min(values_ranges, key=lambda value_range: value_range.start).start
    print(min_location_value)


def part_2(input_text: str):
    print("Part 2")

    seed_line, *mapping_records = input_text.split("\n\n")
    mappings = parse_mappings(mapping_records)
    seeds_values = [int(seed) for seed in seed_line.split(": ")[1].split()]
    seed_ranges = [
        Range(seed_start, seed_start + seed_length)
        for seed_start, seed_length in zip(seeds_values[::2], seeds_values[1::2])
    ]

    values_ranges = seed_ranges
    for mapping in mappings:
        values_ranges = [r for r in yield_mapped_ranges(mapping, values_ranges) if r.start < r.end]

    min_location_value = min(values_ranges, key=lambda value_range: value_range.start).start
    print(min_location_value)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
