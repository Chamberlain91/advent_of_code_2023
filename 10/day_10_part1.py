# Christopher Chamberlain
# Advent of Code 2023
# Day 10.1

from collections import deque
from dataclasses import dataclass


class Ansi:

    BLACK = "\033[0;30m"

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"

    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"

    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    LIGHT_YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"

    WHITE = "\033[1;37m"

    def RGB(r: int, g: int, b: int): return f"\033[38;2;{r};{g};{b}m"
    def BACKGROUND_RGB(r: int, g: int, b: int): return f"\033[48;2;{r};{g};{b}m"

    RESET_COLORS = "\033[0m"

    def SET_CURSOR(x: int, y: int): return f"\033[{y};{x}H"
    SAVE_CURSOR = f"\0337"
    RESTORE_CURSOR = f"\0338"

    HIDE_CURSOR = f"\033[?25l"
    SHOW_CURSOR = f"\033[?25h"

    ERASE_SCREEN = "\033[2J"
    CLEAR_SCREEN = "\033[3J"


@dataclass
class PipeInfo:

    character: str
    glyph: str
    connections: list[list[str]]
    neighbors: list[int]


type Coord = tuple[int, int]
type Grid[T] = dict[Coord, T]


def add_coord(c0: Coord, c1: Coord) -> Coord:
    """ Adds two coordinates together. """
    return (c0[0] + c1[0], c0[1] + c1[1])


# All 8-direction neighbors.
NEIGHBOR_OFFSETS: list[Coord] = [(0, -1), (+1, 0), (0, +1), (-1, 0)]

# The allowable symbols for connection in each direction.
T_CONNECTIONS = ['|', '7', 'F']
C_CONNECTIONS = ['-', '7', 'J']
B_CONNECTIONS = ['|', 'L', 'J']
L_CONNECTIONS = ['-', 'F', 'L']

# The table of information for each pipe tile.
PIPE_TABLE = {p.character: p for p in [
    # ...
    PipeInfo('|', '│', [T_CONNECTIONS, [], B_CONNECTIONS, []], [0, 2]),
    PipeInfo('-', '─', [[], C_CONNECTIONS, [], L_CONNECTIONS], [1, 3]),
    PipeInfo('L', '└', [T_CONNECTIONS, C_CONNECTIONS, [], []], [0, 1]),
    PipeInfo('7', '┐', [[], [], B_CONNECTIONS, L_CONNECTIONS], [2, 3]),
    PipeInfo('F', '┌', [[], C_CONNECTIONS, B_CONNECTIONS, []], [1, 2]),
    PipeInfo('J', '┘', [T_CONNECTIONS, [], [], L_CONNECTIONS], [0, 3]),
    # ...
    PipeInfo('.', ' ', [[], [], [], []], []),
    PipeInfo('S', 'S', [[], [], [], []], [0, 1, 2, 3]),
]}


# Read input data.
with open("day_10_input.txt", encoding='utf-8') as file:
    input = file.read().splitlines()

grid: Grid[PipeInfo] = {}
start: Coord


def get_grid(grid: Grid[PipeInfo], x: int, y: int) -> PipeInfo:
    return grid[(x, y)] if (x, y) in grid else PIPE_TABLE['.']


def draw_pipes(grid: Grid[PipeInfo], distances: Grid[int]):

    screen_buffer = ""

    screen_buffer += Ansi.HIDE_CURSOR
    screen_buffer += Ansi.SET_CURSOR(0, 0)

    H = len(input)
    W = len(input[0])

    # Parse input data.
    for y in range(0, H):
        for x in range(0, W):

            pipe = grid[(x, y)]

            if (x, y) in distances:
                screen_buffer += Ansi.BLUE
            else:
                screen_buffer += Ansi.WHITE

            screen_buffer += pipe.glyph

        screen_buffer += "\n"

    screen_buffer += Ansi.RESET_COLORS
    screen_buffer += Ansi.SHOW_CURSOR

    print(screen_buffer)


# Parse input data.
for y, line in enumerate(input):
    for x, symbol in enumerate(line):

        # Populate pipe grid.
        grid[(x, y)] = PIPE_TABLE[symbol]

        # Store starting position.
        if symbol == 'S':
            start = (x, y)

assert start

# First figure out the starting pipe, by evaluating connectivity with its neighbors.
common = set(PIPE_TABLE.keys())
for i, (dx, dy) in enumerate(NEIGHBOR_OFFSETS):
    i_opposite = (i + 2) % 4
    if (pipe := get_grid(grid, start[0] + dx, start[1] + dy)) and pipe.connections[i_opposite]:
        common.intersection_update(pipe.connections[i_opposite])

assert len(common) == 1

# Replace the start pipe with the correct pipe tile.
grid[start] = PIPE_TABLE[list(common)[0]]

# ...
distances: Grid[int] = {}
iteration: int = 0

# We will begin evaluating the connectivity from the starting position.
queue = deque[tuple[Coord, int]]()
queue.append((start, 0))

# Find the tiles connected to the "loop" with an expanding frontier.
while queue and (element := queue.pop()):
    coord, distance = element

    # Mark this position as visited.
    distances[coord] = distance

    # For each neighboring position.
    for n in grid[coord].neighbors:

        # Compute neighbor position.
        n_coord = add_coord(coord, NEIGHBOR_OFFSETS[n])

        if n_coord not in distances:
            queue.appendleft((n_coord, distance + 1))
            distances[n_coord] = -1

    # Display the pipe network each 200 steps.
    if iteration % 200 == 0:
        draw_pipes(grid, distances)

    iteration += 1

# Display final frame.
draw_pipes(grid, distances)

# Find the largest distance, this is the answer.
print(distances[max(distances, key=lambda key: distances[key])])  # 6909
