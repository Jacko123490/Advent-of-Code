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
def get_button_press(button: int, out_len: int) -> list[int]:
    """Get the power state from pressing a button."""
    out = [0] * out_len
    for i, b in enumerate(bin(button)[::-1]):
        if b == "b":
            break
        elif b == "1":
            out[i] = 1
    return out


@cache
def get_button_indices(button: int) -> list[int]:
    """Get indices for affected outputs from a button press."""
    ind = []
    for i, b in enumerate(bin(button)[::-1]):
        if b == "b":
            break
        elif b == "1":
            ind.append(i)
    return ind


def press_button_jolts(buttons: list[int], presses: Iterable[int], out_len: int) -> list[int]:
    """Compute jolts from pressing a set of buttons different numbers of times."""
    out = [0] * out_len
    for button, count in zip(buttons, presses):
        for i, press in enumerate(get_button_press(button, out_len)):
            out[i] += press * count
    return out


def compare_joltage(buttons: list[int], presses: Iterable[int], expected: list[int]) -> tuple[bool, bool, list[int]]:
    """Compares the joltage to a test value. Second value determines if any joltage under/overshoots target.

    :returns: (is_equal, is_underjolted)
    """
    out = press_button_jolts(buttons, presses, len(expected))
    is_underjolt = False
    for test_i, result_i in zip(out, expected):
        if test_i > result_i:
            return False, False, out
        elif test_i < result_i:
            is_underjolt = True
    return not is_underjolt, is_underjolt, out


def depth_press_search(buttons: list[int], joltage: list[int]) -> Iterator[tuple[bool, tuple[int, ...]]]:
    """Search through all possible presses depth first on each press.
    Upper limit of each buttons search range is derived from the joltage results.
    """
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


def prune_depth_press_search(buttons: list[int], joltage: list[int]) -> list[list[int]]:
    """Search through all possible presses depth first on each press.
    Results are pruned once a depth tree surpasses any joltage limit.
    Upper limit of each buttons search range is derived from the joltage results.
    """
    # Collect max presses for each button to limit iteration output
    button_max = [min([joltage[j] for j in get_button_indices(b)]) for b in buttons]
    print("Button combinations: ", button_max)
    results = []
    solution_count = pruning_iterator(buttons, joltage, [0] * len(buttons), [range(value + 1) for value in button_max], results)
    print("Checked: ", solution_count, ", Pruned: ", max(joltage) ** len(buttons) - solution_count)
    return results


def pruning_iterator(buttons: list[int], joltage: list[int], press: list[int], iterators: list[Iterable[int]], results: list[list[int]]) -> int:
    """Generates test presses for each combination of iterator provided for each button.
    Invalid presses will prune generation of future presses in that chain.
    """
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
        for i, ind in enumerate(get_button_press(b, len(joltage))):
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


def breadth_press_search(start_press: list[int], press_level: int, buttons: list[int], expected: list[int]) -> tuple[list[list[int]], int]:
    """Takes a starting press value and generates branches which increment press values for this branch.
    To avoid re-computing the same branches, only the press values for the current level are incremented.
    """
    # Exit condition
    # print(start_press)
    solve_count = 1
    match, underjolt, test = compare_joltage(buttons, start_press, expected)
    if match:  # This is a valid solution, return this result and stop this branch
        return [start_press], solve_count
    else:
        if not underjolt:  # This branch has overshot a valid result, prune tree here
            return [], solve_count
        else:  # This branch has undershot the result, expand the tree from here
            # Generate every combination of values to update for this press_level
            # Ie. for this branch only update values i where start_press[i] = press_level
            increment_options: list[list[int]] = []
            for combo in itertools.product([0, 1], repeat=start_press.count(press_level)):  # generate every combination of +1 and +0 for each press value to update
                new_press: list[int] = []
                update_count = 0
                for i in start_press:
                    if i == press_level:  # Update press count
                        new_press.append(i + combo[update_count])
                        update_count += 1
                    else:  # Copy press count
                        new_press.append(i)
                if new_press != start_press:  # Dont duplicate input
                    increment_options.append(new_press)

            # For each option, compute and append results from subtrees
            valid_presses: list[list[int]] = []
            for press in increment_options:
                new_presses, new_count = breadth_press_search(press, press_level + 1, buttons, expected)
                valid_presses += new_presses
                solve_count += new_count
            return valid_presses, solve_count


@cache
def part(n: int, maxsize: int, ind=1) -> list[list[int]]:
    """Generate all partitions for integer n."""
    result = [[n]]
    for i in range(ind, n//2 + 1):
        for p in part(n-i, maxsize, i):
            value = p + [i]
            if len(value) <= maxsize:
                result.append(p + [i])
    return result


def get_permutations_for_sum(target: int, n: int) -> Iterator[tuple[int, ...]]:
    """Computes all unique permutations of n numbers which sum to a target value."""
    for sum_set in part(target, n):  # get partition for sum to generate all unique combinations of integers
        if len(sum_set) <= n:  # partitions with less digits can be padded as zero values are allowed
            sum_set = sum_set + [0] * (n - len(sum_set))
            for combo in set(itertools.permutations(sum_set)):  # Add all permutations of this set of numbers
                yield combo


def prune_permutations_to_press(jolt: int, jolt_map: list[int],
                                buttons: list[int], joltage: list[int]) -> Iterator[list[int]]:
    """Get all the permutations of buttons which give the required joltage and prune them to remove invalid presses."""
    for perm in get_permutations_for_sum(jolt, len(jolt_map)):
        # Build press for this permutation
        press = [0] * len(buttons)
        for press_count, b_i in zip(perm, jolt_map):
            press[b_i] = press_count

        # Check if permutation overshoots joltage
        #   When pressing buttons, some combinations may overshoot power for other outputs
        match, underjolt, test = compare_joltage(buttons, press, joltage)
        if match or underjolt:
            yield press


def compute_valid_presses(buttons: list[int], expected: list[int]) -> Iterator[list[int]]:
    """Generate the set of valid presses such that each joltage value is satisfied individually."""
    solution_count = 0
    jolt_map: list[list[int]] = [[] for _ in range(len(expected))]
    for i, b in enumerate(buttons):
        for ind in get_button_indices(b):
            jolt_map[ind].append(i)

    # For each possible jolt output, generate a combination of buttons which matches it ('get_permutations_for_sum(jolt, len(buttons))')
    #   Then iterate over every combination of jolt combinations and see which ones can agree on a press array
    for press_sets in itertools.product(*[prune_permutations_to_press(jolt, button_ind, buttons, expected)
                                          for jolt, button_ind in zip(expected, jolt_map)]):
        # Generate net press by combining the press for each jolt combination
        #   - Also check if press sets from each jolt combination align
        press = [0] * len(buttons)
        is_valid = True
        for press_add in press_sets:
            if not is_valid:
                break
            for i, press_val in enumerate(press_add):
                if press_val:
                    # Check for conflicting values if both are non-zero
                    if press[i] and not (is_valid := press[i] == press_val):
                        break
                    press[i] = press_val

        solution_count += 1
        # print(press)
        if is_valid:
            print(press)
            yield press
    print("Checked: ", solution_count, ", Pruned: ", max(joltage) ** len(buttons) - solution_count)


# Get data
machines: list[tuple[int, list[int], list[int]]] = []
with open("inputs/d10_input.txt") as file:
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
print(f"Day 10 Problem 1: {p1_count}")  # 491

# Collect valid presses
valid_presses_p2: list[list[list[int]]] = []
for i, (result, buttons, joltage) in enumerate(machines):
    print(f"[{i+1}/{len(machines)}]\tSolving joltage: {joltage} from buttons: {buttons}")
    valid_presses: list[list[int]] = []
    for press in compute_valid_presses(buttons, joltage):
        match, underjolt, test = compare_joltage(buttons, press, joltage)
        if match:
            valid_presses.append(press)
        pass
    valid_presses_p2.append(valid_presses)

    '''solve_count: int
    valid_presses, solve_count = breadth_press_search([0] * len(buttons), 0, buttons, joltage)
    print("Checked: ", solve_count, ", Pruned: ", max(joltage) ** len(buttons) - solve_count)'''



    '''valid_presses: list[tuple[int, ...]] = []
    
    # Iterate over each combination of button presses
    result = prune_check_test_set(buttons, joltage)
    valid_presses_p2.append(result)
    print("Results: ", result)
    for match, press in generate_test_set(buttons, joltage):
        if match:
            valid_presses.append(press)
    print("Results: ", valid_presses)
    valid_presses_p2.append(valid_presses)'''
print(valid_presses_p2)

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

print(f"Day 10 Problem 2: {sum(p2_results)}")  #
