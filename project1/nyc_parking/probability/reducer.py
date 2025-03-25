#!/usr/bin/env python3
import sys

counts = {"black_vehicle": 0, "total_black_vehicles": 0}

for line in sys.stdin:
    key, value = line.strip().split("\t")
    counts[key] += int(value)

# Compute probability
if counts["total_black_vehicles"] > 0:
    probability = counts["black_vehicle"] / counts["total_black_vehicles"]
else:
    probability = 0.0

print(f"Probability of black vehicle getting a ticket: {probability:.4f}")

