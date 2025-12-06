# -*- coding: utf-8 -*-
"""
2025 Day 3 Problems
3/12/2025 6:46 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "3/12/2025 6:46 pm"
__version__ = "1.0"
__copyright__ = __author__


def get_max_value(values: list[int], n: int) -> str:
    """Retrieves the largest possible length n string of digits from a set."""
    if n <= 0:
        return ""
    else:
        subset = values[:len(values)+1-n]
        # print(len(values), len(subset), subset)
        i = subset.index(max_val := max(subset))
        return str(max_val) + get_max_value(values[i+1:], n-1)


p1_jolt = 0
p2_jolt = 0
with open("inputs/d3_input.txt") as file:
    for line in file.readlines():
        line = line.strip()
        batt = [int(i) for i in line]

        # P1: Compute largest 2 digits
        max_batt = batt[:-1].index(max(batt[:-1]))
        max_batt2 = batt[max_batt + 1:].index(max(batt[max_batt + 1:])) + max_batt + 1
        print(f"{line}\nMax 1: line[{max_batt}] = {batt[max_batt]}\nMax 2: line[{max_batt2}] = {batt[max_batt2]}")
        assert max_batt2 > max_batt, \
            "Second digit retrieved before the last."
        if max_batt2 != len(batt) - 1:
            assert batt[max_batt] >= batt[max_batt2], \
                (f"First digit (line[{max_batt}] = {batt[max_batt]}) is not the largest. "
                 f"Second digit is: line[{max_batt2}] = {batt[max_batt2]}")
        jolt = int(f"{batt[max_batt]}{batt[max_batt2]}")
        p1_jolt += jolt

        # P2: Generalise to largest n digits
        jolt = int(get_max_value(batt, 12))
        p2_jolt += jolt

print(f"Day 3 Problem 1: {p1_jolt}")  # 17113
print(f"Day 3 Problem 2: {p2_jolt}")  # 169709990062889
