#!/usr/bin/env python3

from collections import Counter
from dataclasses import dataclass
from enum import Enum


class Card(Enum):
    JOKER = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


CARD_MAP = {
    "2": Card.TWO,
    "3": Card.THREE,
    "4": Card.FOUR,
    "5": Card.FIVE,
    "6": Card.SIX,
    "7": Card.SEVEN,
    "8": Card.EIGHT,
    "9": Card.NINE,
    "T": Card.TEN,
    "J": Card.JACK,
    "Q": Card.QUEEN,
    "K": Card.KING,
    "A": Card.ACE,
}


class Rank(Enum):
    HIGH = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    FULL = 5
    FOUR = 6
    FIVE = 7


@dataclass
class Hand:
    cards: list[Card]
    rank: Rank
    bid: int

    def __init__(self, line: str, with_jokers=False):
        hand_str, bid_str = line.split(" ")
        self.bid = int(bid_str)
        self.cards = [CARD_MAP[card] for card in hand_str]

        if with_jokers:
            self.cards = [Card.JOKER if card == Card.JACK else card for card in self.cards]

        card_count = Counter(self.cards)
        self.rank = self.get_best_rank(card_count)

    def get_best_rank(self, card_count: Counter):
        if len(card_count) == 5:
            # With a single joker this hand can be upgraded to a pair
            rank = Rank.ONE_PAIR if card_count[Card.JOKER] == 1 else Rank.HIGH
        elif len(card_count) == 4:
            # With one or two jokers this hand can be upgraded to a three of a kind
            if card_count[Card.JOKER] == 1 or card_count[Card.JOKER] == 2:
                rank = Rank.THREE_KIND
            else:
                rank = Rank.ONE_PAIR
        elif len(card_count) == 3:
            # With 1 joker and 2 pairs this hand can be upgraded to a full house, otherwise to a four of a kind
            if card_count[Card.JOKER] > 0:
                if card_count[Card.JOKER] == 1 and 3 not in card_count.values():
                    rank = Rank.FULL
                else:
                    rank = Rank.FOUR
            elif 3 in card_count.values():
                rank = Rank.THREE_KIND
            else:
                rank = Rank.TWO_PAIR
        elif len(card_count) == 2:
            # With any number of jokers this hand can be upgraded to a five of a kind
            if card_count[Card.JOKER] > 0:
                rank = Rank.FIVE
            elif 4 in card_count.values():
                rank = Rank.FOUR
            else:
                rank = Rank.FULL
        elif len(card_count) == 1:
            rank = Rank.FIVE
        else:
            raise ValueError(f"Invalid card count: {card_count}")
        return rank

    def __gt__(self, other: "Hand"):
        if self.rank != other.rank:
            return self.rank.value > other.rank.value
        else:
            for card, other_card in zip(self.cards, other.cards):
                if card.value != other_card.value:
                    return card.value > other_card.value
            return False


def part_1(input_text: str):
    print("Part 1")
    hands = [Hand(line) for line in input_text.split("\n")]
    # sort hands by rank, then by cards
    hands.sort()
    total = sum(hand.bid * (rank + 1) for rank, hand in enumerate(hands))
    print(total)


def part_2(input_text: str):
    print("Part 2")
    hands = [Hand(line, with_jokers=True) for line in input_text.split("\n")]
    # sort hands by rank, then by cards
    hands.sort()
    total = 0
    total = sum(hand.bid * (rank + 1) for rank, hand in enumerate(hands))
    print(total)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
