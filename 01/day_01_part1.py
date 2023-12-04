# Christopher Chamberlain
# Advent of Code 2023
# Day 1.1

# ----
# Read input data
# ----

with open("day_01_input.txt", encoding='utf-8') as file:
    input = file.readlines()

# ----
# Compute answer
# ----

sum = 0
for line in input:
    digits = [c for c in list(line) if c.isdigit()]
    sum += int("".join([digits[0], digits[-1]]))

print(sum)  # 53194
