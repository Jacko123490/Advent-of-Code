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


def area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Computes the area of a rectangle defined by its two opposite corners."""
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def intersection(l1: tuple[tuple[int, int], tuple[int, int]],
                 l2: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    """Checks if two lines intersect.

    Assumes segments are only horizontal/vertical to simplify calculations.
    """
    l1_p1 = l1[0]
    l1_p2 = l1[1]
    l2_p1 = l2[0]
    l2_p2 = l2[1]

    # Ignore parallel cases
    if ((l1_p1[0] == l1_p2[0] and l2_p1[0] == l2_p2[0])
            or (l1_p1[1] == l1_p2[1] and l2_p1[1] == l2_p2[1])):
        return False

    if l1_p1[0] == l1_p2[0]:  # Line 1 is vertical (line 2 is horizontal)
        return (min(l1_p1[1], l1_p2[1]) < l2_p1[1] < max(l1_p1[1], l1_p2[1])  # Line 2 row lies within line 1
                and min(l2_p1[0], l2_p2[0]) < l1_p1[0] < max(l2_p1[0], l2_p2[0]))  # Line 1 column lies within line 2
    else:  # Line 1 is horizontal (line 2 is vertical)
        return (min(l1_p1[0], l1_p2[0]) < l2_p1[0] < max(l1_p1[0], l1_p2[0])  # Line 2 column lies within line 1
                and min(l2_p1[1], l2_p2[1]) < l1_p1[1] < max(l2_p1[1], l2_p2[1]))  # Line 1 row lies within line 2


def generate_rect(p1: tuple[int, int], p2: tuple[int, int]) -> list[tuple[int, int]]:
    """Generate the coordinates of a rectangle given its opposite corners."""
    return [
        (min(p1[0], p2[0]), min(p1[1], p2[1])),
        (min(p1[0], p2[0]), max(p1[1], p2[1])),
        (max(p1[0], p2[0]), max(p1[1], p2[1])),
        (max(p1[0], p2[0]), min(p1[1], p2[1])),
    ]


def segment_in_polygon(polygon: list[tuple[int, int]], p: tuple[int, int],
                       ps: tuple[int, int], include_bounds: bool) -> bool:
    """Check if the provided point lies within the polygon.

    Computes winding number by counting number of crossings past positive x-axis.
    A winding of 0 about p means that p is not within the polygon.
    Assumes segments are only horizontal/vertical to simplify calculations.

    Boundary cases handled by directly checking if the point lies on the polygon border.
    'include_bounds' will determine if this ic treated as inside/outside the polygon.

    This also checks if the segment: p -> ps connected to the current point (p) intersects
    with any polygon boundaries. So the user should also provide the next point for reference.
    """
    cross = 0
    for i, p1 in enumerate(polygon):
        p2 = polygon[(i + 1) % len(polygon)]
        # Current test segment: (p1, p2)

        # Check if point lies on line
        if p1[0] == p2[0] and p[0] == p1[0]:
            if min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1]):
                return include_bounds
        if p1[1] == p2[1] and p[1] == p1[1]:
            if min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]):
                return include_bounds

        # Check if current segment: p1 -> p2, crosses reference segment: p -> ps
        if intersection((p, ps), (p1, p2)):
            return False

        # Update winding number crossings about p
        if p1[1] == p2[1]:  # Ignore horizontal segments
            continue
        if p[0] < p1[0]:  # only consider crossings past positive x-axis
            if min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1]):  # Does cross ray from p
                count = 1/2 if p[1] in [p1[1], p2[1]] else 1  # Half crossing if segment starts/ends on ray from p
                cross += count if p2[1] > p1[1] else -count  # Check crossing direction
    return not (cross == 0)


def rect_in_polygon(polygon: list[tuple[int, int]], p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    """Determine if the rectangle formed by (p1, p2) lies within the polygon."""
    rect = generate_rect(p1, p2)
    print(f"Rect: {rect}, A: {area(p1, p2)}")

    # Check if rectangle bounds lie outside of the polygon
    for i, p in enumerate(rect):
        p2 = rect[(i + 1) % len(rect)]
        in_poly = segment_in_polygon(polygon, p, p2, True)
        print(f"Rect point {p} in polygon: {in_poly}")
        if not in_poly:
            print(f"Rect not in polygon")
            return False

    # Check if polygon bounds lie inside rectangle
    for i, p in enumerate(polygon):
        p2 = rect[(i + 1) % len(rect)]
        in_rect = segment_in_polygon(rect, p, p2, False)
        print(f"Poly point {p} in rect: {in_rect}")
        if in_rect:
            print(f"Rect not in polygon")
            return False
    print(f"Rect in polygon")
    return True


# Get data
tiles: list[tuple[int, int]] = []  # (x, y)
with open("inputs/d9_input.txt") as file:
    for line in file.readlines():
        line = line.strip()
        tiles.append(tuple(int(i) for i in line.split(",")))

# P1
max_area_p1 = 0
corners: tuple[tuple[int, int], tuple[int, int]]
for p1 in tiles:
    # print(f"P1: {p1}")
    for p2 in tiles:
        if (A := area(p1, p2)) > max_area_p1:
            max_area_p1 = A
            corners = (p1, p2)

print(f"Day 9 Problem 1: {max_area_p1}")  # 4750092396

# P2
max_area_p2 = 0
rects = []
for p1 in tiles:
    # print(f"P1: {p1}")
    for p2 in tiles:
        corners = (p1, p2)
        A = area(*corners)
        if p1 != p2 and A > max_area_p2 and rect_in_polygon(tiles, *corners):
            max_area_p2 = A
            rects.append(corners)

for rect in rects:
    print(f"Rect: {rect}, A: {area(*rect)}")
print(f"Day 9 Problem 2: {max_area_p2} {rects[-1]}")  # 1468516555


# Debug plot
import matplotlib.pyplot as plt

plt.clf()
rect = generate_rect(*rects[-1])
plt.plot([p[0] for p in tiles], [p[1] for p in tiles], "ko-")
plt.plot([p[0] for p in rect], [p[1] for p in rect], "ro-")
plt.show()
