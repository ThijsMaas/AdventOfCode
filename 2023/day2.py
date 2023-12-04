from io import TextIOWrapper


def hand_is_possible(hand_str: str, max_colors: tuple[int, int, int]) -> bool:
    max_red, max_green, max_blue = max_colors
    for color_str in hand_str.split(", "):
        number, color = color_str.split(" ")
        if color == "red":
            if int(number) > max_red:
                return False
        elif color == "green":
            if int(number) > max_green:
                return False
        elif color == "blue":
            if int(number) > max_blue:
                return False
    return True


def game_is_possible(game_str: str, max_colors: tuple[int, int, int]) -> bool:
    for hand_str in game_str.split("; "):
        if not hand_is_possible(hand_str, max_colors):
            return False
    return True


def game_min_cubes(game_str: str):
    game_min = [0, 0, 0]
    for hand_str in game_str.split("; "):
        hand_min = [0, 0, 0]
        for color_str in hand_str.split(", "):
            number, color = color_str.split(" ")
            if color == "red":
                hand_min[0] += int(number)
            elif color == "green":
                hand_min[1] += int(number)
            elif color == "blue":
                hand_min[2] += int(number)
        game_min = [
            max(game_min[0], hand_min[0]),
            max(game_min[1], hand_min[1]),
            max(game_min[2], hand_min[2]),
        ]
    return game_min


def part_1(input_file: TextIOWrapper):
    print("Part 1")
    possible_games = []
    for line in input_file.readlines():
        game_str, hands_str = line.split(":")
        game_idx = int(game_str.split(" ")[1])
        game_str = hands_str.strip()
        if game_is_possible(game_str, (12, 13, 14)):
            possible_games.append(game_idx)
            continue

    print("Possible Games: ", sum(possible_games))


def part_2(input_file: TextIOWrapper):
    print("Part 2")
    power_sum = 0
    for line in input_file.readlines():
        game_str = line.split(":")[1].strip()
        min_red, min_green, min_blue = game_min_cubes(game_str)
        game_power = min_red * min_green * min_blue
        power_sum += game_power
    print("Power Sum: ", power_sum)


def solution(input_file: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input_file)
    elif part_number == 2:
        part_2(input_file)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
