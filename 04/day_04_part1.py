# Christopher Chamberlain
# Advent of Code 2023
# Day 4.1

# Read input data
with open("day_04_input.txt", encoding='utf-8') as file:
    input: list[str] = file.read().splitlines()

answer: int = 0

for line in input:
    card, data = line.split(':')

    # Parse number lists
    win_numbers, our_numbers = data.strip().split('|')
    win_numbers: set[int] = set([int(x) for x in win_numbers.strip().split(' ') if x])
    our_numbers: set[int] = set([int(x) for x in our_numbers.strip().split(' ') if x])

    # Get matching set of numbers
    matching = our_numbers.intersection(win_numbers)

    # Accumulate score.
    answer += 2 ** (len(matching) - 1) if matching else 0

print(answer)  # 27059
