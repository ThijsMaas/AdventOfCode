from io import TextIOWrapper


def part_1(input: TextIOWrapper):
    print("Part 1")
    times = [int(i) for i in input.readline().split()[1:]]
    distances = [int(i) for i in input.readline().split()[1:]]
    multiply = 1
    for race_time, record_distance in zip(times, distances):
        number_of_ways_to_beat = 0
        print(f"{race_time} {record_distance}")
        # Brute force
        for hold_time in range(race_time):
            moving_time = race_time - hold_time
            race_speed = hold_time
            race_distance = race_speed * moving_time
            if race_distance > record_distance:
                number_of_ways_to_beat += 1
        multiply *= number_of_ways_to_beat
    print(multiply)


def part_2(input: TextIOWrapper):
    print("Part 2")
    race_time = int("".join(input.readline().split()[1:]))
    record_distance = int("".join(input.readline().split()[1:]))
    number_of_ways_to_beat = 0
    print(f"{race_time} {record_distance}")
    # Brute force
    for hold_time in range(race_time):
        moving_time = race_time - hold_time
        race_speed = hold_time
        race_distance = race_speed * moving_time
        if race_distance > record_distance:
            number_of_ways_to_beat += 1
    print(number_of_ways_to_beat)


def solution(input: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input)
    elif part_number == 2:
        part_2(input)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
