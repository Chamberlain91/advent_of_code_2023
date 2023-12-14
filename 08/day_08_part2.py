# Christopher Chamberlain
# Advent of Code 2023
# Day 8.2

import math
import re
from collections import deque
from dataclasses import dataclass

NODE_REGEX = re.compile(r"(.+) = \((.+), (.+)\)")


@dataclass
class Node:
    name: str
    left: str
    right: str


# Read input data
with open("day_08_input.txt", encoding='utf-8') as file:
    input = deque(file.read().splitlines())

# Parse LR instructions
instructions = list(input.popleft())
input.popleft()  # skip blank

# Parse network
network = dict[str, Node]()
while input and (match := NODE_REGEX.match(input.popleft())):
    X, L, R = match.groups([1, 2, 3])
    network[X] = Node(X, L, R)


def count_steps(start: Node):

    global instructions
    global network

    # ...
    instruction_queue = deque(instructions)
    current_node = start

    steps = 0
    path = [start.name]

    # Walk the network from 'A' to 'Z'
    while instruction_queue and (instruction := instruction_queue.popleft()):

        # ...
        next_identifier = current_node.left if instruction == 'L' else current_node.right
        current_node = network[next_identifier]

        # ...
        path.append(current_node.name)
        steps += 1

        # ...
        if next_identifier.endswith('Z'):
            break

        # To avoid running out of instructions, populate put on end of deque.
        instruction_queue.append(instruction)

    return steps

# Careful observation of the input data shows all starting nodes produce cycles of exactly the instruction length.
# Which means we can compute the LCM of the lengths of the cycles to compute the total number of steps.
#
#                                                             x
#                                                             x
# 111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
# 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
# 3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3
# 4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4
# 5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5    5
#                                                             x
#                                                             x
#
# Here we can see 1 * 2 * 3 * 4 * 5 = 120 but 2 is a factor of 4, so its actually just 3*4*5 = 60
#


# Gather the starting nodes.
starting_nodes = [network[k] for k in network.keys() if k.endswith("A")]

# Compute the length of each cycle.
path_lengths = list[int]()
for node in starting_nodes:
    path_lengths.append(count_steps(node))

# Compute the least common multiple of these cycles.
lcm = 1
for i in path_lengths:
    lcm = lcm * i // math.gcd(lcm, i)

print(lcm)  # 21003205388413
