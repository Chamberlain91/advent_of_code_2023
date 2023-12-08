# Christopher Chamberlain
# Advent of Code 2023
# Day 6.2

import math

# Read input data
with open("day_06_input.txt", encoding='utf-8') as file:
    input = file.read().splitlines()

# Parse data
t = int(input[0].removeprefix("Time:").replace(' ', ''))
d = int(input[1].removeprefix("Distance:").replace(' ', ''))

'''
The example states:
In the second race, hold for at least 4, at most 11.

(15 - 3) * 3 = 36
(15 - 4) * 4 = 44

Thus:

((t - x) * x) = d
'''

# Compute the roots...?
root = math.sqrt((t * t) - 4 * (d + 0.00000001))
x0, x1 = math.ceil(0.5 * (t - root)), math.ceil(0.5 * (root + t))

print(x1 - x0)  # 34788142
