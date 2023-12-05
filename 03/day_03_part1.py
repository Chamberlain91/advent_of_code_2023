# Christopher Chamberlain
# Advent of Code 2023
# Day 3.1

# Read input data
with open("day_03_example.txt", encoding='utf-8') as file:
    input = file.read().splitlines()

height: int = 0
width: int = 0

grid: dict[tuple[int, int], str] = {}

# Load input into the grid
for y, line in enumerate(input):
    height = max(height, y + 1)
    for x, ch in enumerate(line):
        width = max(height, x + 1)
        grid[(x, y)] = ch

# All 8-direction neighbors.
neighbors: list[tuple[int, int]] = [
    (-1, -1), (0, -1), (+1, -1),
    (-1, 0), (+1, 0),
    (-1, +1), (0, +1), (+1, +1),
]


def get_grid(x: int, y: int) -> str:
    return grid[(x, y)] if (x, y) in grid else '.'


answer: int = 0

y: int = 0
while y < height:

    x: int = 0
    while x < width:

        number: list[str] = []
        symbol: str = ''

        # Attempt to scan a number.
        while (ch := get_grid(x, y)).isdigit():

            # Check each adjacent location to the number
            for (xoffset, yoffset) in neighbors:
                adjacent = get_grid(x + xoffset, y + yoffset)
                if adjacent != '.' and not adjacent.isdigit():
                    symbol = adjacent
                    break

            # Store this digit, accumulate number.
            number.append(ch)
            x += 1

        # If we found a number and a symbol, we have a read part number.
        if number and symbol:
            answer += int("".join(number))

        x += 1

    y += 1


print(answer)  # 554003
