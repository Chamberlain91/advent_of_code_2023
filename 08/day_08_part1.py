# Christopher Chamberlain
# Advent of Code 2023
# Day 8.1

import re
from collections import deque

regex = re.compile(r"(.+) = \((.+), (.+)\)")

# Read input data
with open("day_08_input.txt", encoding='utf-8') as file:
    input = deque(file.read().splitlines())

# Parse LR instructions
instructions = list(input.popleft())
input.popleft()  # skip blank

# Parse network
network = dict[str, tuple[str, str]]()
while input and (match := regex.match(input.popleft())):
    X, L, R = match.groups([1, 2, 3])
    network[X] = [L, R]

# ...
instruction_queue = deque(instructions)
current_node = network['AAA']
steps = 0

# Walk the network.
while instruction_queue and (instruction := instruction_queue.popleft()):

    # ...
    next_identifier = current_node[0 if instruction == 'L' else 1]
    current_node = network[next_identifier]
    steps += 1

    # ...
    if next_identifier == 'ZZZ':
        break

    # If out of instructions, populate the queue again.
    if not instruction_queue:
        instruction_queue = deque(instructions)

print(steps)  # 19631
