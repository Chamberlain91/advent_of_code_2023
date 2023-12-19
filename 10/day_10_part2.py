# Christopher Chamberlain
# Advent of Code 2023
# Day 10.2

from collections import deque
from dataclasses import dataclass
from enum import IntEnum
from itertools import product as cartesian_product

ANIM_STEPS = 1000


class Category(IntEnum):
    Unknown = 0
    Loop = 1
    LoopWalk = 2
    Inside = 3
    Outside = 4


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
    ERASE_TO_BOTTOM = "\033[0J"
    ERASE_TO_TOP = "\033[1J"
    ERASE_LINE = "\033[2K"

    CLEAR_SCREEN = "\033[3J"


@dataclass
class PipeInfo:

    character: str
    glyph: str
    connections: list[list[str]]
    neighbors: list[int]
    neighbors_edge: list[int]


type Coord = tuple[int, int]
type Grid[T] = dict[Coord, T]


def add_coord(c0: Coord, c1: Coord) -> Coord:
    """ Performs element-wise addition. """
    return (c0[0] + c1[0], c0[1] + c1[1])


def sub_coord(c0: Coord, c1: Coord) -> Coord:
    """ Performs element-wise subtraction. """
    return (c0[0] - c1[0], c0[1] - c1[1])


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
    PipeInfo('|', '│', [T_CONNECTIONS, [], B_CONNECTIONS, []], [0, 2], [1, 3]),
    PipeInfo('-', '─', [[], C_CONNECTIONS, [], L_CONNECTIONS], [1, 3], [0, 2]),
    PipeInfo('L', '└', [T_CONNECTIONS, C_CONNECTIONS, [], []], [0, 1], [2, 3]),
    PipeInfo('7', '┐', [[], [], B_CONNECTIONS, L_CONNECTIONS], [2, 3], [0, 1]),
    PipeInfo('F', '┌', [[], C_CONNECTIONS, B_CONNECTIONS, []], [1, 2], [0, 3]),
    PipeInfo('J', '┘', [T_CONNECTIONS, [], [], L_CONNECTIONS], [0, 3], [1, 2]),
    # ...
    PipeInfo('.', '•', [[], [], [], []], [], []),
    PipeInfo('S', 'S', [[], [], [], []], [], []),
]}

# ...
print(Ansi.HIDE_CURSOR, end='')

# Read input data.
with open("day_10_input.txt", encoding='utf-8') as file:
    input_data = file.read().splitlines()

# Get input dimensions.
H = len(input_data)
W = len(input_data[0])

# ...
grid: Grid[PipeInfo] = {}
start: Coord


def get_grid(grid: Grid[PipeInfo], x: int, y: int) -> PipeInfo:
    return grid[(x, y)] if (x, y) in grid else PIPE_TABLE['.']


def draw_pipes(grid: Grid[PipeInfo], categories: Grid[Category]):

    screen_buffer = ""
    screen_buffer += Ansi.SET_CURSOR(0, 0)

    # Parse input data.
    for y in range(0, H):
        for x in range(0, W):

            match categories.get((x, y), None):
                case Category.Loop:
                    screen_buffer += Ansi.BLUE
                case Category.LoopWalk:
                    screen_buffer += Ansi.WHITE
                case Category.Inside:
                    screen_buffer += Ansi.GREEN
                case Category.Outside:
                    screen_buffer += Ansi.RED
                case Category.Unknown:
                    screen_buffer += Ansi.YELLOW
                case _:
                    screen_buffer += Ansi.DARK_GRAY

            screen_buffer += grid[(x, y)].glyph
        screen_buffer += "\n"

    screen_buffer += Ansi.RESET_COLORS
    print(screen_buffer.strip())


# Parse input data.
for y, line in enumerate(input_data):
    for x, symbol in enumerate(line):

        # Populate pipe grid.
        grid[(x, y)] = PIPE_TABLE[symbol]

        # Store starting position.
        if symbol == 'S':
            start = (x, y)

assert start

# First figure out the starting pipe, by evaluating connectivity with its neighbors.
common = set(PIPE_TABLE.keys())
for iteration, offset in enumerate(NEIGHBOR_OFFSETS):
    i_opposite = (iteration + 2) % 4
    if (pipe := grid.get(add_coord(start, offset))) and pipe.connections[i_opposite]:
        common.intersection_update(pipe.connections[i_opposite])

assert len(common) == 1

# Replace the start pipe with the correct pipe tile.
grid[start] = PIPE_TABLE[list(common)[0]]

# The category of each tile.
categories: Grid[Category] = {}

# The looping pipe path.
path = list[Coord]()

# We will begin evaluating the connectivity from the starting position.
frontier = deque[tuple[Coord, int]]()
frontier.append((start, Category.Loop))

# Find the tiles connected to the "loop" with an expanding frontier.
while frontier and (element := frontier.pop()):
    co, category = element
    path.append(co)

    # Mark this position as visited.
    categories[co] = category

    # For each neighboring position.
    for n in grid[co].neighbors:

        # Compute neighbor position.
        if (n_co := add_coord(co, NEIGHBOR_OFFSETS[n])) and not n_co in categories:
            frontier.append((n_co, Category.Loop))

        if len(path) % ANIM_STEPS == 0:
            draw_pipes(grid, categories)

# ...
draw_pipes(grid, categories)

# Computes coordinates for all tiles and all non-loop tiles.
all_grid_locations = set(cartesian_product(range(0, W), range(0, H)))
unknown_locations = all_grid_locations - set(categories.keys())

# Mark each non-loop location as Unknown.
for co in unknown_locations:
    categories[co] = Category.Unknown

# Walks along "outside wall" and marks each neighbor as either 'inside' or 'outside'.
# Note: Inside and Outside may not actually be true inside and outside,
# however, they do correctly classify each side of the loop.
for index, co in enumerate(path):
    categories[co] = Category.LoopWalk

    # Compute delta offsets for current and next steps.
    delta_curr = sub_coord(co, path[index - 1])
    delta_next = sub_coord(path[(index + 1) % len(path)], co)

    # Compute perpendiculars...
    perp1 = (delta_curr[1], -delta_curr[0])
    perp2 = (-delta_curr[1], delta_curr[0])

    # ...
    if index % ANIM_STEPS == 0:
        draw_pipes(grid, categories)

    def flood(co: Coord, category: Category):

        queue = deque[Coord]()
        queue.append(co)

        while queue and (co := queue.pop()):

            # Assign category.
            categories[co] = category

            # Submit Unknown neighbors.
            for offset in NEIGHBOR_OFFSETS:
                if (n_co := add_coord(co, offset)) in categories and categories[n_co] == Category.Unknown:
                    categories[n_co] = category
                    queue.appendleft(n_co)

    # Mark the perpendicular edges along the path as "inside" or "outside"
    for offset in [NEIGHBOR_OFFSETS[n] for n in grid[co].neighbors_edge]:
        n_co = add_coord(co, offset)
        if n_co in categories and categories[n_co] == Category.Unknown:
            is_outside = offset == perp2 or delta_next == perp1
            flood(n_co, Category.Outside if is_outside else Category.Inside)

# Display final frame.
draw_pipes(grid, categories)

# ...
print(Ansi.SHOW_CURSOR, end='')

# Count how many inside tiles we have.
print("Outside:", list(categories.values()).count(Category.Outside))  # 461
print("Inside:", list(categories.values()).count(Category.Inside))  # 5321
