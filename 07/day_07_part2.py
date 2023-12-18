# Christopher Chamberlain
# Advent of Code 2023
# Day 7.2

from dataclasses import dataclass
from enum import IntEnum
from functools import total_ordering
from typing import List


def compare[T](this: T, that: T) -> int:
    """
    Compares two comparable values, returning -1, 0, or +1
    """

    if this == that:
        return 0

    return -1 if this < that else +1


# Card information.
card_by_index = reversed(['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'])  # 0 -> A
index_by_card = {card: index for index, card in enumerate(card_by_index)}  # A -> 0


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

    def natural_type(self) -> HandType:
        """
        Determines the "natural" hand type, not accounting for Joker subsitution.
        """

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

    def type(self) -> HandType:
        """
        Determines the hand type, accounting for Joker subsitution.
        """

        cards_without_a_sense_of_humor = [c for c in self.cards if c != 'J']
        if not cards_without_a_sense_of_humor:
            return HandType.FiveOfKind  # All cards were (J)okers

        # Switch out J cards for the card we have the most of that is not a J card.
        max_card = max(cards_without_a_sense_of_humor, key=lambda card: cards_without_a_sense_of_humor.count(card))
        psuedo_cards = [(max_card if c == 'J' else c) for c in self.cards]

        return Hand(psuedo_cards, self.bid).natural_type()

    def compare(self, that: 'Hand') -> int:

        this_type = self.type()
        that_type = that.type()

        # Compare types (first priority)
        if (compare_type := compare(this_type, that_type)) and compare_type != 0:
            return compare_type

        # Compare cards (secondary priority)
        for i in range(0, len(self.cards)):

            # Get each card rank
            this_card = index_by_card[self.cards[i]]
            that_card = index_by_card[that.cards[i]]

            if (compare_card := compare(this_card, that_card)) and compare_card != 0:
                return compare_card

        return 0  # all things appear equal

    def __lt__(self, other: 'Hand') -> bool:
        return self.compare(other) < 0

    def __eq__(self, other: 'Hand') -> bool:
        return self.compare(other) == 0


# Read input data.
with open("day_07_input.txt", encoding='utf-8') as file:
    input = file.read().splitlines()

# Parse input data.
hands = list[Hand]()
for line in input:
    cards, bid = line.split(' ')
    hands.append(Hand(list(cards), int(bid)))

# Sort the hands.
hands.sort()

# Accumulate score in rank order.
score = 0
for rank, hand in enumerate(hands):
    score += (rank + 1) * hand.bid

print(score)  # 246436046
