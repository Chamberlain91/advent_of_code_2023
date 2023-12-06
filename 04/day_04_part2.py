# Christopher Chamberlain
# Advent of Code 2023
# Day 4.2

from collections import deque
from dataclasses import dataclass


@dataclass
class Card:
    copies: int
    score: int


# Read input data
with open("day_04_input.txt", encoding='utf-8') as file:
    input: list[str] = file.read().splitlines()

# Parse game cards
cards = deque[Card]()
for game, line in enumerate(input):
    card, data = line.split(':')

    # Parse number lists
    win_numbers, our_numbers = data.strip().split('|')
    win_numbers: set[int] = set([int(x) for x in win_numbers.strip().split(' ') if x])
    our_numbers: set[int] = set([int(x) for x in our_numbers.strip().split(' ') if x])

    # Compute matching set of numbers, this is the "score" of the card
    cards.append(Card(1, len(our_numbers.intersection(win_numbers))))

answer: int = 0

# Process game
while len(cards) > 0:

    # Get next card to process
    card = cards.popleft()

    # Add copies
    for i in range(0, card.score):
        cards[i].copies += card.copies

    # Finished this card
    answer += card.copies

print(answer)  # 5744979
