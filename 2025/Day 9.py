# -*- coding: utf-8 -*-
"""
2025 Day 9 Problems
9/12/2025 2:51 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "9/12/2025 2:51 pm"
__version__ = "1.0"
__copyright__ = __author__

import math as m

# Get data
tiles: list[tuple[int, int]] = []  # (x, y)
with open("inputs/d9_input_ref.txt") as file:
    for line in file.readlines():
        line = line.strip()

        tiles.append(tuple(int(i) for i in line.split(",")))


def area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0] + 1) * abs(p1[1] - p2[1] + 1)


# P1
max_area_p1 = 0
corners: tuple[tuple[int, int], tuple[int, int]]
for p1 in tiles:
    print(f"P1: {p1}")
    for p2 in tiles:
        if (A := area(p1, p2)) > max_area_p1:
            max_area_p1 = A
            corners = (p1, p2)

print(f"Day 9 Problem 1: {max_area_p1}")  # 4750092396

# P2
def in_rect(p: tuple[int, int], p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    return (min(p1[0], p2[0]) < p[0] < max(p1[0], p2[0])
            and  min(p1[1], p2[1]) < p[1] < max(p1[1], p2[1]))

def through_rect(pl1: tuple[int, int], pl2: tuple[int, int], p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    """Check if line passes through rect"""
    x_start, x_stop = min(p1[0], p2[0]), max(p1[0], p2[0])
    y_start, y_stop = min(p1[1], p2[1]), max(p1[1], p2[1])

    if pl1[0] == pl2[0]:  # column line
        if x_start < pl1[0] < x_stop: # Infinite line passes through rect
            start, stop = min(p1[1], p2[1]), max(p1[1], p2[1])
            return start < y_stop and stop > y_start  # Finite line passes through rect
        else:
            return False
    else:  # row line
        if y_start < pl1[1] < y_stop: # Infinite line passes through rect
            start, stop = min(p1[0], p2[0]), max(p1[0], p2[0])
            return start < x_stop and stop > x_start  # Finite line passes through rect
        else:
            return False


def contains_rect(polygon: list[tuple[int, int]], p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    for i, p in enumerate(polygon):
        pn = polygon[(i+1)%len(polygon)]
        if through_rect(p, pn, p1, p2):
            return False
    return True


def point_in_polygon(polygon: list[tuple[int, int]], p: tuple[int, int], include_bounds: bool) -> bool:
    # Implement winding number algorithm
    cross = 0
    for i, pi in enumerate(polygon):
        p1 = polygon[(i + 1) % len(polygon)]

        if pi[1] == p1[1]:
            continue
        if p[0] <= pi[0]:
            # Check crossing
            if min(pi[1], p1[1]) <= p[1] <= max(pi[1], p1[1]):
                count = 1/2 if p[1] in [pi[1], p1[1]] else 1 # Half crossing if starts/ends on ray
                if p1[1] > pi[1]:
                    cross += count
                else:
                    cross -= count
    return not (cross == 0)


def generate_rect(p1: tuple[int, int], p2: tuple[int, int]) -> list[tuple[int, int]]:
    return [
        (min(p1[0], p2[0]), min(p1[1], p2[1])),
        (min(p1[0], p2[0]), max(p1[1], p2[1])),
        (max(p1[0], p2[0]), max(p1[1], p2[1])),
        (max(p1[0], p2[0]), min(p1[1], p2[1])),
    ]


max_area_p2 = 0
for p1 in tiles:
    print(f"P1: {p1}")
    for p2 in tiles:
        if p1 != p2 and (A := area(p1, p2)) > max_area_p2:
            if all([point_in_polygon(tiles, p, True) for p in generate_rect(p1, p2)]) \
                and not any([point_in_polygon(generate_rect(p1, p2), p, False) for p in tiles]):
                max_area_p2 = A
                corners = (p1, p2)

print(f"Day 9 Problem 2: {max_area_p2}")  #
