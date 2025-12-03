# -*- coding: utf-8 -*-
"""
2025 Day 1 Problems
4/12/2025 9:34 am
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "4/12/2025 9:34 am"
__version__ = "1.0"
__copyright__ = __author__

zeros_p1 = 0
zeros_p2 = 0
position = 50
size = 100
with open("inputs/d1_input.txt", "r") as file:
    for line in file.readlines():
        line = line.strip()
        direction = 1 if line[0] == "R" else -1
        move = int(line[1:])
        # print(direction, move)

        for i in range(move):
            position += direction
            position %= size
            if position == 0:
                zeros_p2 += 1
        if position == 0:
            zeros_p1 += 1
print(f"D1 P1: {zeros_p1}")  # 1089
print(f"D1 P2: {zeros_p2}")  # 6530
