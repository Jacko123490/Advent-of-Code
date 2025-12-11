# -*- coding: utf-8 -*-
"""
2025 Day 10 Problems
10/12/2025 1:30 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "10/12/2025 1:30 pm"
__version__ = "1.0"
__copyright__ = __author__

import itertools
from sympy import Matrix, linsolve
from copy import copy
from collections.abc import Iterable, Iterator
from functools import cache


def press_button_lights(buttons: list[int], presses: int) -> int:
    """Simulate button presses turning on/off lights by flipping bitmasks for each button.
    As presses are commutative, pressing any button more than once is equivalent to pressing it only once or not at all.
    This means that any combination of button presses can be represented as a single bitmask for which buttons to press.

    :param buttons: list of button wirings, each wiring is a bitmask for what lights are connected
    :param presses: Which buttons to press
    """
    result = 0
    # Need to iterate backwards through press bitstring as that is how bits are represented
    for i, b in enumerate(bin(presses)[::-1]):
        if b == "b":
            break
        elif b == "1":
            # Simulate light flip using XOR for each bit in button mask
            result = result ^ buttons[i]
    return result


@cache
def get_button_press(button: int, press: int, jolt_len: int) -> list[int]:
    out = [0] * jolt_len
    for i, b in enumerate(bin(button)[::-1]):
        if b == "b":
            break
        elif b == "1":
            out[i] = press
    return out


@cache
def get_button_indices(button: int) -> list[int]:
    ind = []
    for i, b in enumerate(bin(button)[::-1]):
        if b == "b":
            break
        elif b == "1":
            ind.append(i)
    return ind


def press_button_jolts(buttons: list[int], presses: Iterable[int], jolt_len: int) -> list[int]:
    out = [0] * jolt_len
    for button, count in zip(buttons, presses):
        for i, press in enumerate(get_button_press(button, count, jolt_len)):
            out[i] += press
    return out


def compare_joltage(buttons: list[int], presses: Iterable[int], expected: list[int]) -> tuple[bool, bool, list[int]]:
    """Compares the joltage to a test value. Second value determines if any joltage under/overshoots target.

    :returns: (is_equal, is_underjolted)
    """
    out = press_button_jolts(buttons, presses, len(expected))
    for test_i, result_i in zip(out, expected):
        if test_i > result_i:
            return False, False, out
        elif test_i < result_i:
            return False, True, out
    return True, False, out


def generate_test_set(buttons: list[int], joltage: list[int]) -> Iterator[tuple[bool, tuple[int, ...]]]:
    # Collect max presses for each button to limit iteration output
    button_max = [min([joltage[j] for j in get_button_indices(b)]) for b in buttons]
    print("Button combinations: ", button_max)

    # Iterate over each combination of button presses, limited by known maximums
    solution_count = 0
    for press in itertools.product(*[range(value + 1) for value in button_max]):
        solution_count += 1
        match, underjolt, test = compare_joltage(buttons, press, joltage)
        yield match, press
    print("Checked: ", solution_count, ", Pruned: ", max(joltage) ** len(buttons) - solution_count)


def prune_check_test_set(buttons: list[int], joltage: list[int]) -> list[list[int]]:
    # Collect max presses for each button to limit iteration output
    button_max = [min([joltage[j] for j in get_button_indices(b)]) for b in buttons]
    print("Button combinations: ", button_max)
    results = []
    solution_count = pruning_iterator(buttons, joltage, [0] * len(buttons), [range(value + 1) for value in button_max], results)
    print("Checked: ", solution_count, ", Pruned: ", max(joltage) ** len(buttons) - solution_count)
    return results


def pruning_iterator(buttons: list[int], joltage: list[int], press: list[int], iterators: list[Iterable[int]], results: list[list[int]]) -> int:
    checked_values = 0
    ind = len(buttons) - len(iterators)
    press = copy(press)
    for i in iterators[0]:
        press[ind] = i
        # print(press)
        checked_values += 1
        match, underjolt, test = compare_joltage(buttons, press, joltage)
        if match:
            results.append(copy(press))
        else:
            if underjolt:
                if len(iterators) > 1:
                    checked_values += pruning_iterator(buttons, joltage, press, iterators[1:], results)
    return checked_values


def button_solutions(buttons: list[int], joltage: list[int]) -> list[list[int]]:
    """Try to solve problem using linear equation systems."""
    A = [[] for _ in range(len(joltage))]
    for b in buttons:
        for i, ind in enumerate(get_button_press(b, 1, len(joltage))):
            A[i].append(ind)
        # A.append(np.array(get_button_press(b, 1, len(joltage))).reshape((-1, 1)))
    #  = np.concatenate(A, axis=1)
    A = Matrix(A)
    b = Matrix([[i] for i in joltage])
    result_set = linsolve((A, b))
    results = []
    for result in result_set:
        result = [i.subs([("tau0", -1), ("tau1", -1)]) for i in result]
        assert press_button_jolts(buttons, result, len(joltage)) == joltage
        temp2 = sum(result)
        results.append(result)
    temp = results
    return results


# Replaced by alternate loop with pruning
def test_joltage_set(start_press: tuple[int], buttons: list[int], expected: list[int]) -> list[tuple[int]]:
    """Increment every combination of non-zero elements in the start_press and check its joltage.
    Recursively tests each result which is underjolted and returns any matching sets.
    """
    # Exit condition
    match, underjolt, test = compare_joltage(buttons, start_press, expected)
    if match:  # This is a valid solution, return this result and stop this branch
        return [start_press]
    else:
        if not underjolt:  # This branch has overshot a valid result, prune tree here
            return []
        else:  # This branch has undershot the result, expand the tree from here

            # Generate every possible combination of additional presses from this start
            increment_options = []
            increment_count = sum((1 for i in start_press if i != 0))
            for i in range(1, 1 << increment_count):
                press_count = bin(i)[:1:-1]
                for _ in range(increment_count - len(press_count)):  # Pad zeros
                    press_count += "0"
                ind = 0
                new_press = []
                for count in start_press:
                    if count == 0:
                        new_press.append(0)
                    else:
                        new_press.append(count + (1 if press_count[ind] == "1" else 0))
                        ind += 1
                increment_options.append(new_press)

            # For each option append results from subtrees
            valid_presses: list[tuple[int]] = []
            for press in increment_options:
                valid_presses += test_joltage_set(press, buttons, expected)
            return valid_presses


# Get data
machines: list[tuple[int, list[int], list[int]]] = []
with open("inputs/d10_input_ref.txt") as file:
    for line in file.readlines():
        line = line.strip()
        data = line.split()

        result = int(b"".join([b"1" if c == "#" else b"0" for c in data[0].strip("[]")][::-1]), 2)
        joltage = [int(c) for c in data[-1].strip("{}").split(",")]
        buttons = []
        for wiring in data[1:-1]:
            mask = 0
            for c in wiring.strip("()").split(","):
                mask |= 1 << int(c)
            buttons.append(mask)
        machines.append((result, buttons, joltage))

# Print button set
print(machines)
for result, buttons, joltage in machines:
    result = bin(result)
    buttons = [bin(b) for b in buttons]
    print(result, buttons, joltage)

# P1
# Collect valid presses
valid_presses_p1: list[set[int]] = []
for result, buttons, joltage in machines:
    good_press = set()
    valid_presses_p1.append(good_press)
    for i in range(1 << len(buttons)):  # Generate every possible bitmask for button presses
        # print(result, bin(i), press_button_lights(buttons, i))
        if press_button_lights(buttons, i) == result:
            good_press.add(i)
print(valid_presses_p1)

# Determine smallest press count
p1_count = 0
for results in valid_presses_p1:
    print([bin(result).count("1") for result in results])
    p1_count += min([bin(result).count("1") for result in results])

print(f"Day 9 Problem 1: {p1_count}")  # 491

# Collect valid presses
valid_presses_p2: list[list[tuple[int, ...]]] = []
for i, (result, buttons, joltage) in enumerate(machines):
    print(f"[{i+1}/{len(machines)}]\tSolving joltage: {joltage} from buttons: {buttons}")
    valid_presses: list[tuple[int, ...]] = []

    # Iterate over each combination of button presses
    result = prune_check_test_set(buttons, joltage)
    valid_presses_p2.append(result)
    print("Results: ", result)
    '''for match, press in generate_test_set(buttons, joltage):
        if match:
            valid_presses.append(press)
    print("Results: ", valid_presses)'''
    # valid_presses_p2.append(valid_presses)
# print(valid_presses_p2)

p2_results = []
for press_set in valid_presses_p2:
    min_sum = None
    min_press = None
    for result in press_set:
        sum_press = sum(result)
        if min_sum is None or sum_press < min_sum:
            min_sum = sum_press
            min_press = result
    p2_results.append(min_sum)
    print(min_sum, min_press)

print(f"Day 9 Problem 2: {sum(p2_results)}")  #
