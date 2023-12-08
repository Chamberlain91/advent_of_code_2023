# Christopher Chamberlain
# Advent of Code 2023
# Day 5.2

from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class Range:

    begin: int
    end: int

    @property
    def size(self) -> int:
        return self.end - self.begin

    def intersects(self, other: 'Range') -> Optional['Range']:
        '''
        Computes the intersection between this range and another.
        Will return `None` if the ranges are not intersecting.

        ```txt
        self:   |-----|
        other:    |-----|
        result:   |---|
        ```
        '''

        begin = max(self.begin, other.begin)
        end = min(self.end, other.end)

        if begin >= end:
            return None

        return Range(begin, end)


@dataclass
class AlmanacRange:

    _dst: int
    _src: int
    _len: int

    @property
    def src(self) -> Range:
        return Range(self._src, self._src + self._len)

    @property
    def dst(self) -> Range:
        return Range(self._dst, self._dst + self._len)


def compute_mapping(almanacs: list[AlmanacRange], query: Range) -> list[Range]:

    segments = list[Range]()

    # Finds the set of ranges that intersect the query.
    if almanacs := deque(filter(lambda r: query.intersects(r.src) is not None, almanacs)):

        # Begin at the left most edge of the query.
        minEdge = query.begin

        while almanacs:

            '''

            Case A - Intersecting
            |-----------------|    query
               |---|   |---|       almanac
            |--|---|---|---|--|    result

            Case B - Disjoint
            |------|               query
                     |---|  |---|  almanac
            |------|               result

            '''

            # Get next almanac range to process.
            almanac = almanacs.popleft()

            # Compute the intersection of this almanac range and query range.
            intersection = almanac.src.intersects(query)

            # Computes the offset in the almanac src to dst mapping.
            offset = intersection.begin - almanac.src.begin
            assert offset >= 0

            # Append identiy 'gap' segment
            if intersection.begin != minEdge:
                segments.append(Range(minEdge, intersection.begin))

            # Append almanac mapped segment.
            segments.append(Range(almanac.dst.begin + offset, almanac.dst.begin + offset + intersection.size))

            # Advance minimum edge to the end of the intersection.
            minEdge = intersection.end

        # Append trailing identiy 'gap' segment
        if minEdge != query.end:
            segments.append(Range(minEdge, query.end))

    # Query was fully disjoint, does not intersect any almanac range.
    if not segments:
        segments = [query]

    return segments


# List of seeds to evaluate
seed_ranges: list[Range] = []

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
        seed_ranges = [int(x) for x in line.split(":")[1].strip().split(" ")]
        seed_ranges = [Range(x[0], x[0] + x[1]) for x in zip(seed_ranges[0::2], seed_ranges[1::2])]

    # Parse lookup tables.
    elif line:
        # Start building next lookup table.
        if line.endswith("map:"):
            lookup_name = line.split(" ")[0].replace("-", '_')
            lookup_current = locals()[lookup_name]
            lookup_names.append(lookup_name)
        else:
            # Append lookup entry to current table.
            lookup_current.append(AlmanacRange(*[int(x) for x in line.split(" ")]))

# Sort almanac ranges, low to high.
for lookup_name in lookup_names:
    almanacRange: list[AlmanacRange] = locals()[lookup_name]
    almanacRange.sort(key=lambda r: r.src.begin)

best_location: int | None = None

# Search for the best location.
for seed_range in seed_ranges:
    soil_ranges = compute_mapping(seed_to_soil, seed_range)

    for soil_range in soil_ranges:
        fertilizer_ranges = compute_mapping(soil_to_fertilizer, soil_range)

        for fertilizer_range in fertilizer_ranges:
            water_ranges = compute_mapping(fertilizer_to_water, fertilizer_range)

            for water_range in water_ranges:
                light_ranges = compute_mapping(water_to_light, water_range)

                for light_range in light_ranges:
                    temperature_ranges = compute_mapping(light_to_temperature, light_range)

                    for temperature_range in temperature_ranges:
                        humidity_ranges = compute_mapping(temperature_to_humidity, temperature_range)

                        for humidity_range in humidity_ranges:
                            location_ranges = compute_mapping(humidity_to_location, humidity_range)

                            if location_ranges:

                                # Record the best location (lowest value)
                                location = min(location_ranges, key=lambda r: r.begin)
                                if best_location is None or location.begin < best_location:
                                    best_location = location.begin

print(best_location)  # 1240035
