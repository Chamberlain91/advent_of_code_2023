# Christopher Chamberlain
# Advent of Code 2023
# Day 7.2

import math
from dataclasses import dataclass
from enum import IntEnum
from functools import total_ordering
from typing import List

# ...
card_by_index = reversed(['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'])
index_by_card = {card: index for index, card in enumerate(card_by_index)}


@total_ordering
class HandType(IntEnum):
    HighCard = 0  # 23456 (all unique, highest card scores)
    OnePair = 1  # A23A4 (two similar)
    TwoPair = 2  # 23432 (two + two  similar)
    ThreeOfKind = 3  # TTT98 (three  similar)
    FullHouse = 4  # 23332 (three + two similar)
    FourOfKind = 5  # AA8AA (four similar)
    FiveOfKind = 6  # AAAAA (five similar)


@total_ordering
@dataclass
class Hand:
    cards: List[str]
    bid: int

    def type(self) -> HandType:

        unique_cards = set(self.cards)
        unique_count = [self.cards.count(card) for card in unique_cards]
        num_unique_cards = len(unique_count)

        if num_unique_cards == 5:  # 23456 -> 23456
            return HandType.HighCard

        if num_unique_cards == 4:  # AA234 -> A234
            return HandType.OnePair

        if num_unique_cards == 3:  # AAA23 -> A23 or # AABB3 -> A23
            return HandType.ThreeOfKind if max(unique_count) == 3 else HandType.TwoPair

        if num_unique_cards == 2:  # AAA22 -> A2 or AAAA2 -> A2
            return HandType.FourOfKind if max(unique_count) == 4 else HandType.FullHouse

        return HandType.FiveOfKind

    def compare(self, other: 'Hand') -> int:

        self_type = self.type()
        other_type = other.type()

        if self_type == other_type:

            # Secondary Priority - Card Rank
            for i in range(0, len(self.cards)):

                # Get each card rank
                self_card = index_by_card[self.cards[i]]
                other_card = index_by_card[other.cards[i]]

                if self_card != other_card:
                    return math.copysign(1.0, self_card - other_card)

            return 0  # all things appear equal

        # Primary Priority - Hand Type
        return math.copysign(1.0, self_type - other_type)

    def __lt__(self, other: 'Hand') -> bool:
        return self.compare(other) < 0

    def __eq__(self, other: 'Hand') -> bool:
        return self.compare(other) == 0


# Read input data
with open("day_07_input.txt", encoding='utf-8') as file:
    input = file.read().splitlines()

# Parse input data
hands = list[Hand]()
for line in input:
    cards, bid = line.split(' ')
    hands.append(Hand(list(cards), int(bid)))

# Sort the hands
hands.sort()

# ...
score = 0
for rank, hand in enumerate(hands):
    score += (rank + 1) * hand.bid
    print((rank + 1), hand.cards, hand.type().name, hand.bid)

print(score)
