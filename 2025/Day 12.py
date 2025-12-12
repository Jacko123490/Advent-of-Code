# -*- coding: utf-8 -*-
"""
2025 Day 12 Problems
12/12/2025 11:48 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "12/12/2025 11:48 pm"
__version__ = "1.0"
__copyright__ = __author__

import string
import numpy as np
from dataclasses import dataclass
from copy import copy, deepcopy
from functools import cache
from collections.abc import Iterable, Iterator


def rotation_mod(rotation: int) -> int:
    return ((rotation + 1) % 4) - 1


@dataclass
class Point:
    x: int
    y: int

    def rotate(self, rotation: int) -> "Point":
        """Rotates this point about the origin of the shape: (1,1)

        A positive rotation is a 90* clockwise turn of this point about (1,1).
        The rotation variable indicates how many to perform in this direction.
        """
        match rotation:
            case 0:
                return copy(self)
            case 1:
                return Point(1 - (self.y - 1), 1 + (self.x - 1))
            case -1:
                return Point(1 + (self.y - 1), 1 - (self.x - 1))
            case 2:
                return Point(1 - (self.x - 1), 1 - (self.y - 1))
            case _:
                return self.rotate(rotation_mod(rotation))  # Bring rotations into single circle

    def flip(self, horizontal: bool) -> "Point":
        """Flip this point about the origin of the shape: (1,1)
        The flip can be about the horizontal or vertical axis.
        """
        if horizontal:
            return Point(1 - (self.x - 1), self.y)
        else:
            return Point(self.x, 1 - (self.y - 1))

    def flatten(self, size: tuple[int, int]) -> int:
        """Identify the index for this point in a m x n matrix. (size = (n, m))"""
        return size[0] * self.y + self.x

    @classmethod
    def unflatten(cls, ind: int, size: tuple[int, int]) -> "Point":
        """Convert a matrix index into a Point."""
        return Point(ind % size[0], ind // size[1])

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __copy__(self):
        return Point(self.x, self.y)


class Shape:

    def __init__(self, points: Iterable[Point]):
        self.points = set(points)
        self._cache: dict[tuple[Point, int, bool | None], Shape] = {(Point(0, 0), 0, None): self}

    def __str__(self):
        lines = ["." * 3 for _ in range(3)]
        for p in self.points:
            x = p.x % 3
            y = p.y % 3
            lines[y] = lines[y][:x] + "#" + lines[y][x + 1:]
        return "\n".join(lines)

    def __repr__(self):
        return f"Shape({str(self.points)})"

    def transform(self, p: Point = Point(0, 0), rot: int = 0, flip: bool | None = None) -> "Shape":
        key = (p, rot, flip)
        if key in self._cache:
            shape = self._cache[key]
        else:
            points = self.points
            points = [pi.rotate(rot) for pi in points]
            if flip is not None:
                points = [pi.flip(flip) for pi in points]
            points = [pi + p for pi in points]
            shape = Shape(points)
            self._cache[(p, rotation_mod(rot), flip)] = shape
        return shape

    def flatten(self, size: tuple[int, int]) -> list[int]:
        return [p.flatten(size) for p in self.points]

    @classmethod
    def unflatten(cls, ind: list[int], size: tuple[int, int]) -> "Shape":
        return Shape([Point.unflatten(i, size) for i in ind])


# Attempt 1: Brute force all orientations
# -----------------------------------------------------------------------------
def available_points(size: tuple[int, int], map: set[Point]) -> Iterator[Point]:
    for x in range(size[0] - 2):
        for y in range(size[1] - 2):
            if (p := Point(x, y)) not in map:
                yield p


def generate_all_placements(shape: int, size: tuple[int, int], map: set[Point] = None) -> Iterator[Shape]:
    if map is None:
        map = set()
    for flip in [None, True, False]:
        for rot in range(-1, 3):
            for p in available_points(size, map):
                yield shapes[shape].transform(p, rot=rot, flip=flip)


def test_shape(size: tuple[int, int], shapes_left: dict[int, int], map: set[Point] = None) -> tuple[bool, list[Shape]]:
    if map is None:
        map = set()
    for i, count in shapes_left.items():
        if count > 0:
            break
    else:
        return True, []
    shapes_left = copy(shapes_left)
    shapes_left[i] -= 1

    for shape in generate_all_placements(i, size, map):
        if map.isdisjoint(shape.points):  # Can place this shape
            test_map = deepcopy(map)
            test_map.update(shape.points)

            result, soln_shapes = test_shape(size, shapes_left, test_map)
            if result:
                return True, soln_shapes + [shape]
    return False, []


# Attempt 2: Knuths Algorithm
# -----------------------------------------------------------------------------
def generate_cover_matrix(size: tuple[int, int], placement: dict[int, int]) -> np.ndarray:
    i = 0
    rows = []
    shape_count = sum(placement.values())
    for ind, count in placement.items():
        for _ in range(count):
            shape_row = [False] * shape_count
            shape_row[i] = True
            i += 1
            for shape in generate_all_placements(ind, size):
                placement_row = [False] * size[0] * size[1]
                for ind_flat in shape.flatten(size):
                    placement_row[ind_flat] = True
                rows.append(shape_row + placement_row)
    return np.array(rows)


def alg_x(A: np.ndarray) -> bool:
    if A.size == 0:
        return True

    # Get optimal column with minimum ones
    col = np.count_nonzero(A, axis=0).argmin()




# Debugging
def place_shape(shape: Shape, map: set[Point]) -> bool:
    """Places a shape on a map if possible. Returns if this was successful."""
    if map.isdisjoint(shape.points):
        map.update(shape.points)
        return True
    else:
        return False


def print_map(size: tuple[int, int], shapes: list[Shape]) -> str:
    lines = ["." * size[0] for _ in range(size[1])]
    for i, shape in enumerate(shapes):
        chr = get_unique_character(i)
        for p in shape.points:
            lines[p.y] = lines[p.y][:p.x] + chr + lines[p.y][p.x + 1:]
    print("\n".join(lines))


def get_unique_character(ind: int) -> str:
    chars = string.digits + string.ascii_letters + string.punctuation
    return chars[ind % len(chars)]


# Get data
shapes: dict[int, Shape] = {}
regions: list[tuple[tuple[int, int], dict[int, int]]] = []
with open("inputs/d12_input_ref.txt") as file:
    is_shapes = True
    ind = 0
    j = 0
    points = []
    for line in file.readlines():
        line = line.strip()

        if is_shapes:
            if ":" in line:
                if "x" in line:
                    is_shapes = False
                else:
                    ind = int(line.split(":")[0])
                    points = []
                    j = 0
            elif not line:
                shapes[ind] = Shape(points)
            else:
                for i, c in enumerate(line):
                    if c == "#":
                        points.append(Point(i, j))
                j += 1
        if not is_shapes:
            data = line.split(":")
            regions.append((tuple(int(x) for x in data[0].split("x")),
                            {i: int(x) for i, x in enumerate(data[1].strip().split())}))
print(shapes)
print(regions)


# P1
# Brute force
"""
results_p1 = []
for size, placement in regions:
    result, soln_shapes = test_shape(size, placement)
    results_p1.append(result)
    print_map(size, soln_shapes)
"""

# Knuth
temp = shapes[1].transform(Point(1, 0), rot=1)
results_p1 = []
for size, placement in regions:
    temp = generate_cover_matrix(size, placement)
    print(temp.shape, temp)

    result, soln_shapes = test_shape(size, placement)
    results_p1.append(result)
    print_map(size, soln_shapes)

print(f"Day 12 Problem 1: {results_p1.count(True)}")  #
