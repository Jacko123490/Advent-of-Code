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

p1_invalid_ids = []
p2_invalid_ids = []
with open("inputs/d2_input.txt", "r") as file:
    for line in file.readlines():
        # Generate range of IDs
        ids = line.split(",")
        for value in ids:
            start, end = value.split("-")

            for i in range(int(start), int(end) + 1):
                i_str = str(i)

                # P1
                h1, h2 = i_str[:len(i_str) // 2], i_str[len(i_str) // 2:]
                if h1 == h2:
                    p1_invalid_ids.append(i)

                # P2
                # loop through each possible sequence that could repeat and check if it does repeat
                for c_len in range(1, len(i_str) // 2 + 1):
                    test_seq = i_str[:c_len]
                    if len(i_str) % c_len == 0:  # Only consider sub-sequences which divide evenly
                        for ci in range(1, len(i_str) // c_len):  # Check every other sub-sequence for repetition
                            substr = i_str[ci*c_len:ci*c_len+c_len]
                            if substr != test_seq:  # Break early to reduce redundant checks
                                break
                        else:
                            p2_invalid_ids.append(i)
                            break

print(p1_invalid_ids)
print(f"D2 P1: {sum(p1_invalid_ids)}")  # 15873079081
print(f"D1 P2: {sum(p2_invalid_ids)}")  # 22617871034
