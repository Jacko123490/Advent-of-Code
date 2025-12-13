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
from xcover import covers
from numpy.typing import NDArray
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
        return Point(ind % size[0], ind // size[0])

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
    def unflatten(cls, ind: Iterable[int], size: tuple[int, int]) -> "Shape":
        return Shape([Point.unflatten(i, size) for i in ind])


def max_squares_in_rect(n: int, size: tuple[int, int]) -> int:
    """Calculate how many squares of size nxn can fit in a rectangle."""
    return (size[0] // n) * (size[1] // n)


# Attempt 1: Brute force all orientations (far too slow at scale)
# -----------------------------------------------------------------------------
def available_points(size: tuple[int, int], map: set[Point]) -> Iterator[Point]:
    for x in range(size[0] - 2):
        for y in range(size[1] - 2):
            if (p := Point(x, y)) not in map:
                yield p


def generate_all_placements(shape: int, size: tuple[int, int], map: set[Point] = None) -> Iterator[Shape]:
    if map is None:
        map = set()
    for flip in [None, True]:  # Two flips is equivalent to a 180* rotation
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


# Attempt 2: Knuths Algorithm (Custom implementation too slow)
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


def retrieve_alg_x_shapes(rows: np.ndarray, size: tuple[int, int], placement: dict[int, int]) -> list[Shape]:
    shapes = []
    shape_count = sum(placement.values())
    rows = rows[:, shape_count:]
    for row in rows:
        shapes.append(Shape.unflatten(np.argwhere(row).reshape(-1), size))
    return shapes


def alg_x(A: np.ndarray, required_coverage: NDArray[np.bool], row_ind: NDArray[np.int64] = None) -> tuple[bool, list[int]]:
    if row_ind is None:
        row_ind = np.arange(A.shape[0], dtype=int)

    # If empty, valid solution found
    if A.size == 0:
        return True, []

    # Get optimal column with minimum ones, only consider columns which need coverage
    col = np.count_nonzero(A[:, required_coverage], axis=0).argmin()
    if ~np.any(A[:, col]):  # Check if column has any ones, otherwise no rows can cover solution
        return False, []

    # Select each row covering column and create/check subtree
    for row in A[:, col].nonzero()[0]:
        # Select row
        selection = A[row, :]  # Select current row
        selection_ind = row_ind[row]

        # Remove columns that 'row' satisfies and other rows that conflict with 'row'
        A_sub = A
        required_coverage_sub = required_coverage
        row_ind_sub = row_ind
        # - Remove conflicting rows
        valid_rows = ~np.any(np.logical_and(A_sub, selection), axis=1)
        A_sub = A_sub[valid_rows]  # Select rows without any conflicts with selection
        row_ind_sub = row_ind_sub[valid_rows]
        # - Remove covered columns
        A_sub = A_sub[:, ~selection]  # Remove columns covered by selection
        required_coverage_sub = required_coverage_sub[~selection]

        # Check subtree for remaining coverage
        if A_sub.size == 0:  # End condition reached, check if final row selection covers all required columns
            if np.all(selection[required_coverage]):  # Selection covers all required columns
                return True, [selection_ind]
            else:  # Selection does not fulfil coverage, but no valid rows remain to complete this
                continue

        result, rows = alg_x(A_sub, required_coverage_sub, row_ind_sub)
        if result:
            return True, rows + [selection_ind]
    else:
        return False, []


# Attempt 3: Using xcover solver (Faster than my solver, but still too slow to solve this many problems directly)
# -----------------------------------------------------------------------------
def generate_xcover_options(size: tuple[int, int], placement: dict[int, int]) -> tuple[list[list[str]], list[str]]:
    primary = []
    options = []
    for ind, count in placement.items():
        for j in range(count):
            shape_name = f"S{ind}_{j}"
            primary.append(shape_name)
            for shape in generate_all_placements(ind, size):
                options.append([shape_name] + [str(ind_shape) for ind_shape in shape.flatten(size)])
    return options, primary


def retrieve_xcover_shapes(solution: list[list[str]], size: tuple[int, int]) -> list[Shape]:
    shapes = []
    for shape_inds in solution:
        shape_inds = [int(ind) for ind in shape_inds[1:]]
        shapes.append(Shape.unflatten(shape_inds, size))
    return shapes


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
with open("inputs/d12_input.txt") as file:
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

# Modified Knuth
"""
results_p1 = []
for size, placement in regions:
    # Check physical size first
    filled_space = sum(len(shapes[ind].points) * count for ind, count in placement.items())
    if filled_space > size[0] * size[1]:
        print(f"Region {size} cannot fit shapes: {list(placement.values())}")
        results_p1.append(False)
        continue

    A = generate_cover_matrix(size, placement)
    # print(A.shape, A)

    required_coverage = np.zeros(A.shape[1], dtype=bool)
    required_coverage[np.arange(sum(placement.values()), dtype=int)] = True  # Specify required coverage for all shape indices
    result, solution_rows = alg_x(A, required_coverage)

    if result:
        print(f"Arrangement found for region {size} placing shapes: {list(placement.values())}")
        soln_shapes = retrieve_shapes(A[solution_rows], size, placement)
        print_map(size, soln_shapes)
    else:
        print(f"No arrangement found for region {size} placing shapes: {list(placement.values())}")
    results_p1.append(result)
"""

# xcover
results_p1 = []
for i, (size, placement) in enumerate(regions):
    package_count = sum(placement.values())
    print(f"[{i}/{len(regions)}]\tChecking region {size} placing shapes: {list(placement.values())} ({package_count} total)")

    # Check total package space
    filled_space = sum(len(shapes[ind].points) * count for ind, count in placement.items())
    if filled_space > size[0] * size[1]:
        print(f"Shapes cannot fit in region.")
        results_p1.append(False)
        continue

    # Check simple square packing
    square_count = max_squares_in_rect(3, size)
    print(f"Can fit ({square_count}) squares")
    if package_count <= square_count:
        print(f"Shapes pack discretely in region.")
        results_p1.append(True)
        continue

    # Solve Packing
    options, primary = generate_xcover_options(size, placement)
    solution = next(covers(options, primary=primary), None)

    if solution:
        print(f"Arrangement found:")
        soln_shapes = retrieve_xcover_shapes([option for i, option in enumerate(options) if i in solution], size)
        print_map(size, soln_shapes)
        results_p1.append(True)
    else:
        print(f"No arrangement found.")
        results_p1.append(False)

print(f"Day 12 Problem 1: {results_p1.count(True)}")  #
