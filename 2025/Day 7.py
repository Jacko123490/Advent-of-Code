# -*- coding: utf-8 -*-
"""
2025 Day 7 Problems
7/12/2025 3:03 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "7/12/2025 3:03 pm"
__version__ = "1.0"
__copyright__ = __author__

from copy import copy


def update_index(line: str, i: int) -> str:
    """Update a line to display a beam at index i."""
    return line[:i] + "|" + line[i+1:]


# Get data
lines: list[str] = []
with open("inputs/d7_input.txt") as file:
    for line in file.readlines():
        line = line.strip()
        lines.append(line)

# P1
# Count number of times beam splits
p1_count = 0
tachyons: set[int] = set()
filled_lines: list[str] = copy(lines)
for i_line, line in enumerate(lines):
    if "S" in line:
        i = line.index("S")
        tachyons.add(i)
        continue

    for i in copy(tachyons):
        if line[i] == "^":
            tachyons.remove(i)
            tachyons.add(i + 1)
            tachyons.add(i - 1)
            p1_count += 1

    # Update beam display
    for i in tachyons:
        filled_lines[i_line] = update_index(filled_lines[i_line], i)
[print(line) for line in filled_lines]

# P2
# Many Worlds interpretation: Every split creates 2 beams, even if 2 beams split into the same column
#   Therefore, count number of beams in each column rather than columns with beams
mw_tachyons: dict[int, int] = {}
for line in lines:
    if "S" in line:
        i = line.index("S")
        mw_tachyons[i] = 1
        continue

    for i in copy(mw_tachyons):
        if line[i] == "^":
            count = mw_tachyons.pop(i)
            for i_new in [i - 1, i + 1]:
                if i_new in mw_tachyons:
                    mw_tachyons[i_new] += count
                else:
                    mw_tachyons[i_new] = count
print(mw_tachyons)

print(f"Day 7 Problem 1: {p1_count}")  # 1587
print(f"Day 7 Problem 2: {sum([value for value in mw_tachyons.values()])}")  # 5748679033029
