# -*- coding: utf-8 -*-
"""
2025 Day 6 Problems
6/12/2025 3:02 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "6/12/2025 3:02 pm"
__version__ = "1.0"
__copyright__ = __author__

import math as m

# IMPORTANT! Need to remove any trailing whitespace removal in IDE before running.
#   Column widths in reference files need to be the same number of characters,
#   So add spaces until all columns are filled to largest row
input_data = "inputs/d6_input.txt"

# P1
# - Collect data
p1_values: list[list[int]] = []
p1_operations: list[str] = []
with open(input_data) as file:
    for line in file.readlines():
        line = line.strip()

        # Initialise value list
        line_data = line.split()
        if len(line_data) != len(p1_values):
            for i in range(len(line_data)):
                p1_values.append([])

        # Collect values into sets
        for i, value in enumerate(line_data):
            if value.isdigit():
                p1_values[i].append(int(value))
            else:
                p1_operations.append(value)

# - Solve operations
p1_results = []
for operation, value_set in zip(p1_operations, p1_values):
    # Re-read values for P2
    p2_value_set = []
    for value in value_set:
        value_str = str(value)

    match operation:
        case "+":
            p1_results.append(sum(value_set))
        case "*":
            p1_results.append(m.prod(value_set))
print(p1_results, p1_values)

# P2
# - Collect data
lines: list[str] = []
with open(input_data) as file:
    for line in file.readlines():
        lines.append(line.strip("\n"))

# - Collect operations and row widths
p2_operations: list[tuple[str, int]] = []
space_count = 0
operation = None
for c in lines[-1]:
    if c.isspace():
        space_count += 1
    else:
        if operation is not None:
            p2_operations.append((operation, space_count))
        space_count = 0
        operation = c
else:
    p2_operations.append((operation, space_count + 1))

# - Collect values by column
p2_values: list[list[str]] = [["" for _ in range(count)] for _, count in p2_operations]
# for (_, count), value_set in zip(operations, values):
for line in lines[:-1]:
    column_count = 0
    subcolumn_count = 0

    # Add digits from each column
    for c in line:
        if c.isdigit():
            p2_values[column_count][subcolumn_count] += c

        subcolumn_count += 1
        if subcolumn_count > p2_operations[column_count][1]:
            column_count += 1
            subcolumn_count = 0

# - Solve operations
p2_results = []
for (operation, _), value_set in zip(p2_operations, p2_values):
    value_set = [int(value) for value in value_set]
    match operation:
        case "+":
            p2_results.append(sum(value_set))
        case "*":
            p2_results.append(m.prod(value_set))
print(p2_results, p2_values)

print(f"Day 6 Problem 1: {sum(p1_results)}")  # 4693419406682
print(f"Day 6 Problem 2: {sum(p2_results)}")  # 9029931401920
