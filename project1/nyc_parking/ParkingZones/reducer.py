#!/usr/bin/env python3
import sys
from collections import defaultdict
from sklearn.cluster import KMeans
import numpy as np

street_counts = defaultdict(int)

# Read input and aggregate counts
for line in sys.stdin:
    try:
        street_code, count = line.strip().split("\t")
        if street_code.isdigit():  # Ensure street code is numeric
            street_counts[street_code] += int(count)
    except ValueError:
        continue  # Skip invalid lines

# Convert street codes to numerical format for clustering
street_codes = np.array([[int(code)] for code in street_counts.keys()])

# Ensure we have enough data points for clustering
num_clusters = min(10, len(street_codes))
if len(street_codes) == 0:
    print("ERROR: No valid numeric street codes found.", file=sys.stderr)
    sys.exit(1)

if num_clusters > 1:
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto')
    clusters = kmeans.fit_predict(street_codes)
else:
    clusters = [0] * len(street_codes)  # Assign all to one cluster if not enough points

# Assign street codes to clusters
cluster_dict = defaultdict(list)
for i, code in enumerate(street_codes):
    cluster_dict[clusters[i]].append((code[0], street_counts[str(code[0])]))

# Sort clusters by total violations (ascending: least violations first)
sorted_clusters = sorted(cluster_dict.items(), key=lambda x: sum(c[1] for c in x[1]))

# Ensure we have at least one valid cluster
if not sorted_clusters:
    print("ERROR: No clusters were formed.", file=sys.stderr)
    sys.exit(1)

# Pick the best (least violation) cluster
best_cluster, streets = sorted_clusters[0]  # Get the cluster with the least violations
total_violations = sum(c[1] for c in streets)

# Sort streets by violation count (ascending) and get top 5
top_streets = sorted(streets, key=lambda x: x[1])[:5]

# Output the best parking suggestion
print("=== Best Parking Cluster Near Lincoln Center at 10 AM ===")
print(f"Cluster {best_cluster} (Total Violations: {total_violations}):")
for street_code, count in top_streets:
    print(f"  - Street Code: {street_code}, Violations: {count}")

