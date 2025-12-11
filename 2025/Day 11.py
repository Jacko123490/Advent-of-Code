# -*- coding: utf-8 -*-
"""
2025 Day 11 Problems
11/12/2025 4:11 pm
@author: Jacob Wilkinson
"""
__author__ = "Jacob Wilkinson"
__email__ = "jacob.r.wilkinson45@gmail.com"
__date__ = "11/12/2025 4:11 pm"
__version__ = "1.0"
__copyright__ = __author__

from functools import cache


# Get data
device_ports: dict[str, list[str]] = {}
with open("inputs/d11_input.txt") as file:
    for line in file.readlines():
        line = line.strip()
        data = line.split(":")
        connections = data[1].strip().split()

        device_ports[data[0]] = connections
print(device_ports)


@cache
def route_connection(start: str, end: str) -> list[list[str]]:
    """Work out the routes from this start device to a desired endpoint.
    Runs depth-first search through all outgoing connections and appends computed routes from each destination.
    """
    routes = []
    temp = device_ports[start]
    for connection_i in device_ports[start]:
        if connection_i == end:
            # Return route to desired endpoint
            routes.append([start, end])
        elif connection_i == "out":
            pass
        else:
            # Add routes from all destinations and add this as a new source for each
            for route in route_connection(connection_i, end):
                routes.append([start] + route)
    return routes


# P1
# Iterate through all paths from you -> out
p1_routes = route_connection("you", "out")
for route in p1_routes:
    print(" -> ".join(route))
print(f"Day 11 Problem 1: {len(p1_routes)}")  # 772

# P2
# Given one-way network, we can combine possible routes between each required stop
#   rather than iterating through all possible routes.
# Testing shows that no routes exist from dac -> fft so this ordering is the only way to get valid routes
p2_routes_a = route_connection("svr", "fft")  # All ways to get from svr -> fft
p2_routes_b = route_connection("fft", "dac")  # All ways to get from fft -> dac
p2_routes_c = route_connection("dac", "out")  # All ways to get from dac -> out

# Show that no routes exist via other possible paths
p2_routes_d = route_connection("dac", "fft")  # All ways to get from dac -> fft (No routes)

print(f"Day 11 Problem 2: {len(p2_routes_a) * len(p2_routes_b) * len(p2_routes_c)}")  # 423227545768872
