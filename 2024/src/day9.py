from dataclasses import dataclass
from itertools import zip_longest
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing

EXAMPLE_INPUT = """\
2333133121414131402
"""


@timing
def part1(input_data: str):
    disk = []
    it = iter(input_data.strip())
    for block_i, (block_size, space_size) in enumerate(zip_longest(it, it, fillvalue=0)):
        disk.extend([block_i] * int(block_size))
        disk.extend([None] * int(space_size))

    index_offset = 0
    try:
        while True:
            space_index = disk.index(None, index_offset)
            last_file = disk.pop()
            if last_file is None:
                # We dont care about the free space at the end of the disk
                continue
            disk[space_index] = last_file
            index_offset = space_index
    except ValueError:
        return sum(i * file_id for i, file_id in enumerate(disk))


@dataclass
class File:
    id: int
    size: int
    space_after: int

    def __repr__(self):
        return f"{str(self.id)*self.size}{'.'*self.space_after}"


@timing
def part2(input_data: str):
    disk: list[File] = []
    it = iter(input_data.strip())
    for block_i, (block_size, space_size) in enumerate(zip_longest(it, it, fillvalue=0)):
        disk.append(File(block_i, int(block_size), int(space_size)))

    file_id = block_i
    file_offset = len(disk)

    def get_file_index(file_id: int, file_offset: int = 0):
        for i, file in enumerate(disk[::-1], start=file_offset):
            if file.id == file_id:
                return len(disk) - 1 - i + file_offset
        raise IndexError

    while file_id != 0:
        file_index = get_file_index(file_id, file_offset)
        file_to_move = disk[file_index]
        # Check if block fits in space starting from front
        for i in range(file_index):
            if disk[i].space_after >= file_to_move.size:
                moved_file = disk.pop(file_index)
                moved_file_total_size = moved_file.size + moved_file.space_after
                moved_file.space_after = disk[i].space_after - file_to_move.size
                # Replace space after with file
                disk.insert(i + 1, moved_file)
                disk[i].space_after = 0
                # Replace old position with space
                disk[file_index].space_after += moved_file_total_size
                break
        file_id -= 1
        file_offset += 1

    answer = 0
    index = 0
    for file in disk:
        for _ in range((file.size)):
            answer += file.id * index
            index += 1
        index += file.space_after
    return answer


if __name__ == "__main__":
    """Main script to run the solutions, use flag 'e' for the example input and 's' to submit"""
    year, day = list(map(int, re.search(r"(\d{4})/src/day(\d+).py", __file__).groups()))

    # Get input data
    if len(argv) == 2 and argv[1] == "e":
        input_data = EXAMPLE_INPUT
    else:
        input_data = get_input(year, day)

    # Get answers and submit
    answer1 = part1(input_data)
    print(f"Answer part 1: {answer1}")
    if len(argv) == 2 and argv[1] == "s" and answer1 is not None:
        assert submit_answer(year, day, 1, answer1)

    answer2 = part2(input_data)
    print(f"Answer part 2: {answer2}")
    if len(argv) == 2 and argv[1] == "s" and answer2 is not None:
        assert submit_answer(year, day, 2, answer2)
