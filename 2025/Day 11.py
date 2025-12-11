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


# Get data
start_ports: list[str] = []
device_ports: dict[str, list[str]] = {}
with open("inputs/d11_input_ref.txt") as file:
    for line in file.readlines():
        line = line.strip()
        data = line.split(":")
        connections = data[1].strip().split()

        if "you" in connections:
            start_ports.append(data[0])
            connections.remove("you")
        device_ports[data[0]] = connections
print(start_ports, device_ports)

