# -*- coding: utf-8 -*-
"""
2025 Day 3 Problems
4/12/2025 9:40 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "4/12/2025 9:40 pm"
__version__ = "1.0"
__copyright__ = __author__

from copy import deepcopy


def remove_rolls(rack: list[list[bool]]) -> tuple[int, list[list[bool]]]:
    removals: list[tuple[int, int]] = []
    max_neighbors = 4  # Need < 4 neighbors to remove
    neighbor = [-1, 0, 1]

    # Loop through rack
    for i in range(len(rack)):
        for j in range(len(rack[i])):
            # Check if roll can be removed
            if rack[i][j]:
                # Count all neighbors
                neighbor_count = 0
                for i_add in neighbor:
                    for j_add in neighbor:
                        # Discard out_of bounds results
                        if (i_add == 0 and j_add == 0
                                or not (0 <= i + i_add < len(rack))
                                or not (0 <= j + j_add < len(rack[i]))):
                            continue

                        # Count neighbor
                        if rack[i + i_add][j + j_add]:
                            neighbor_count += 1

                # Mark roll for removal
                if neighbor_count < max_neighbors:
                    removals.append((i, j))

    # Remove rolls
    out_rack = deepcopy(rack)
    for i, j in removals:
        out_rack[i][j] = False
    return len(removals), out_rack


# Collect data
rack: list[list[bool]] = []
with open("inputs/d4_input.txt") as file:
    for line in file.readlines():
        line = line.strip()
        rack.append([True if i == "@" else False for i in line])

p1_count, _ = remove_rolls(rack)

p2_count = 0
removals = 1
while removals:
    removals, rack = remove_rolls(rack)
    p2_count += removals

print(f"Day 4 Problem 1: {p1_count}")  # 1460
print(f"Day 4 Problem 2: {p2_count}")  # 9243
