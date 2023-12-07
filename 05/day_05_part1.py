# Christopher Chamberlain
# Advent of Code 2023
# Day 5.1

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class AlmanacRange:
    dst: int
    src: int
    len: int


def find[T](items: List[T], predicate: Callable[[], bool]) -> T | None:
    ''' Finds the first item that matches the predicate. '''
    return next(filter(predicate, items), None)


def find_range(items: List[AlmanacRange], value: int) -> int | None:
    ''' Gets the input value mapped to a target value via the ranges given. '''
    range = find(items, lambda range: (value >= range.src) and (value <= (range.src + range.len)))
    return (range.dst + (value - range.src)) if range is not None else value


# List of seeds to evaluate
seeds: list[int] = []

# Look up tables of ranges, that map to subsequent ranges.
seed_to_soil: list[AlmanacRange] = []
soil_to_fertilizer: list[AlmanacRange] = []
fertilizer_to_water: list[AlmanacRange] = []
water_to_light: list[AlmanacRange] = []
light_to_temperature: list[AlmanacRange] = []
temperature_to_humidity: list[AlmanacRange] = []
humidity_to_location: list[AlmanacRange] = []

# Read input data
with open("day_05_input.txt", encoding='utf-8') as file:
    input = file.read().splitlines()

# Parser state.
lookup_current: list[AlmanacRange] | None = None
lookup_names: list[str] = []

# Parse input data.
for line in input:

    # Parse seed list.
    if line.startswith("seeds"):
        seeds = [int(x) for x in line.split(":")[1].strip().split(" ")]

    # Parse lookup tables.
    elif line:
        # Start building next lookup table.
        if line.endswith("map:"):
            lookup_name = line.split(" ")[0].replace("-", '_')
            lookup_current = locals()[lookup_name]
            lookup_names.append(lookup_name)
        else:
            # Append lookup entry to current table.
            dst, src, len = [int(x) for x in line.split(" ")]
            lookup_current.append(AlmanacRange(int(dst), int(src), int(len)))


best_location: int | None = None

# Evaluate each seed to find the best location.
for seed in seeds:

    # Follow the ranges all the way down.
    soil = find_range(seed_to_soil, seed)
    fertilizer = find_range(soil_to_fertilizer, soil)
    water = find_range(fertilizer_to_water, fertilizer)
    light = find_range(water_to_light, water)
    temperature = find_range(light_to_temperature, light)
    humidity = find_range(temperature_to_humidity, temperature)
    location = find_range(humidity_to_location, humidity)

    # Record the best location.
    if best_location is None or location < best_location:
        best_location = location

print(best_location)  # 650599855
