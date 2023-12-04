from dataclasses import dataclass
from io import TextIOWrapper


@dataclass
class Card:
    index: int
    my_numbers: set[int]
    winning_numbers: set[int]
    copies: int = 1

    def __repr__(self):
        return f"Card({self.index + 1}, copies: {self.copies})"

    def get_winning_amount(self):
        return len(self.my_numbers.intersection(self.winning_numbers))


def get_card_points(winning_numbers: int):
    if winning_numbers < 3:
        return winning_numbers
    return 2 ** (winning_numbers - 1)


def yield_cards(input: TextIOWrapper):
    for i, line in enumerate(input.readlines()):
        my_numbers_str, winning_numbers_str = line.split(":")[1].split("|")
        my_numbers = set(int(num) for num in my_numbers_str.split())
        winning_numbers = set(int(num) for num in winning_numbers_str.split())
        yield Card(i, my_numbers, winning_numbers)


def part_1(input: TextIOWrapper):
    print("Part 1")
    sum_winning = 0
    for card in yield_cards(input):
        sum_winning += get_card_points(card.get_winning_amount())
    print(f"Sum winning: {sum_winning}")


def part_2(input: TextIOWrapper):
    print("Part 2")
    cards = [card for card in yield_cards(input)]
    cards_played = 0
    while cards:
        card = cards.pop(0)
        for copy_card in cards[: card.get_winning_amount()]:
            copy_card.copies += card.copies
        cards_played += card.copies
    print(f"Cards played: {cards_played}")


def solution(input: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input)
    elif part_number == 2:
        part_2(input)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
