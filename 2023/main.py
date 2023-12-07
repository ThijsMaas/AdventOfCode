from importlib import import_module
from sys import argv


def main():
    day_number = argv[1]
    part_number = int(argv[2]) if len(argv) == 3 else 1

    for i in range(1, 26):
        if day_number == str(i):
            day_module = import_module(f"day{i}")
            input_data = f"data/day{i}.txt"
            with open(input_data, "r") as input_file:
                day_module.solution(input_file, part_number)
                break


if __name__ == "__main__":
    main()
