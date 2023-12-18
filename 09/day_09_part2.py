# Christopher Chamberlain
# Advent of Code 2023
# Day 9.2


from pprint import pprint


def compute_derivative(values: list[int]) -> list[int]:
    output = []

    for i in range(1, len(values)):
        output.append(values[i] - values[i - 1])

    return output


def extrapolate(values: list[int]) -> int:

    derivatives = list[list[int]]()
    derivatives.append(values)

    while any(derivatives[-1]):
        derivatives.append(compute_derivative(derivatives[-1]))

    C = 0

    for i in range(len(derivatives) - 1, 0, -1):

        B = derivatives[i][0]
        A = B - C
        C = A

    return values[0] - C


# Read input data.
with open("day_09_input.txt", encoding='utf-8') as file:
    input = file.read().splitlines()

answer = 0

# Predict next value.
for line in input:
    values = [int(x) for x in line.split(' ')]
    answer += extrapolate(values)

print(answer)  # 1062
