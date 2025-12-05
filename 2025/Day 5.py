# -*- coding: utf-8 -*-
"""
2025 Day 5 Problems
5/12/2025 3:03 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "5/12/2025 3:03 pm"
__version__ = "1.0"
__copyright__ = __author__

# Collect data
p1_count = 0
fresh: list[tuple[int, int]] = []
with open("inputs/d5_input.txt") as file:
    is_fresh = True
    for line in file.readlines():
        # Check for dataset change
        line = line.strip()
        if not line:
            is_fresh = False
            continue

        # Add fresh IDs to set
        if is_fresh:
            start, end = line.split("-")
            start, end = int(start), int(end)
            assert end >= start, f"Range not in right order: {end} >= {start}"
            fresh.append((start, end))

        # Check if existing IDs are fresh
        else:
            id = int(line)
            for start, end in fresh:
                if start <= id <= end:
                    p1_count += 1
                    break


# Combine overlaping sets
fresh.sort(key=lambda x: x[0]) # Filter sets by first value

new_fresh: list[tuple[int, int]] = []
start, end = fresh[0]  # Initialise running set
for i, (f_start, f_end) in enumerate(fresh[1:]):
    # running set is separate from current one,
    #   add it and assign current set to running set
    if end < f_start:
        new_fresh.append((start, end))
        start, end = f_start, f_end

    # Running set overlaps with current set
    #   Update running set to accommodate both
    else:
        start = min(start, f_start)
        end = max(end, f_end)
else:
    new_fresh.append((start, end))

fresh = new_fresh
p2_count = sum(len(range(start, end + 1)) for start, end in fresh)  # Get fresh range count

print(f"Day 5 Problem 1: {p1_count}")  # 679
print(f"Day 5 Problem 2: {p2_count}")  # 358155203664116
