# -*- coding: utf-8 -*-
"""
2025 Day 8 Problems
8/12/2025 3:01 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "8/12/2025 3:01 pm"
__version__ = "1.0"
__copyright__ = __author__

import numpy as np
from scipy.spatial.distance import cdist

# Get data
connections = 1000
temp = []
with open("inputs/d8_input.txt") as file:
    for line in file.readlines():
        line = line.strip()
        temp.append(np.array([float(x) for x in line.split(",")]))

# Build distance map
junctions = np.stack(temp)
distance_map = cdist(junctions, junctions)
distance_map[np.tril_indices(distance_map.shape[0])] = 0  # Remove repetitions
print(junctions)
print(distance_map.size, distance_map)

# Get indices of sorted distances
i_sort = np.argsort(distance_map, axis=None)
# - Remove 0 values
remove_list = []
for i in range(i_sort.size):
    if distance_map[np.unravel_index(i_sort[i], distance_map.shape)] == 0:
        remove_list.append(i)
i_sort = np.delete(i_sort, remove_list)
print(i_sort)
print(distance_map[np.unravel_index(i_sort, distance_map.shape)])


# Connect 1000 circuits
def connect_circuits(connection: tuple[int, int], circuits: list[list[int]], singles: set[int]) -> None:
    combine_set = []
    for endpoint in connection:
        if endpoint in singles:
            singles.remove(endpoint)
            combine_set.append(int(endpoint))
        else:
            for j in range(len(circuits)):
                if endpoint in circuits[j]:
                    combine_set.extend(circuits.pop(j))
                    break
    circuits.append(combine_set)


circuits = []
single_junctions = set(range(len(junctions)))
for i in range(connections):  # Get closest junction pairs to connect into circuit
    connect = np.unravel_index(i_sort[i], distance_map.shape)
    connect_circuits(connect, circuits, single_junctions)
circuits.extend([[j] for j in single_junctions])
circuits.sort(key=lambda x: len(x), reverse=True)

print(single_junctions, circuits)
print(f"Day 8 Problem 1: {int(np.prod([len(x) for x in circuits[:3]]))}")  # 127551

# Continue connecting circuits until all junctions are connected
while len(circuits) != 1 and len(single_junctions) > 0:
    # This 'while' condition gives right answer but there are still multiple circuits? (May be issue with answers)
    # Actual condition: 'len(circuits) != 1 or len(single_junctions) > 0',
    #   will terminate once all single junctions are connection AND all circuits are in 1

    i += 1
    connect = np.unravel_index(i_sort[i], distance_map.shape)
    connect_circuits(connect, circuits, single_junctions)
print(single_junctions, circuits)
print(f"Day 8 Problem 2: {int(junctions[connect[0]][0] * junctions[connect[1]][0])}")  # 2347225200
