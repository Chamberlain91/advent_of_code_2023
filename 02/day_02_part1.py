# Christopher Chamberlain
# Advent of Code 2023
# Day 2.1

# Read input data
with open("day_02_input.txt", encoding='utf-8') as file:
    input = file.readlines()

answer = 0

# Game N: subset 1; subset 2;
for n, line in enumerate(input):
    header, subsets = line.split(':')

    counts = {
        'red': 0,
        'blue': 0,
        'green': 0,
    }

    # Parse the game number
    game_number = int(header[5:])

    # Parse the game subsets
    subsets = subsets.strip().split(';')

    for subset in subsets:
        choices = subset.strip().split(',')
        for choice in choices:
            count, color = choice.strip().split(' ')
            counts[color] = max(counts[color], int(count))

    # Game is possible
    if (counts['red'] <= 12) and (counts['green'] <= 13) and (counts['blue'] <= 14):
        answer += game_number

print(answer)
