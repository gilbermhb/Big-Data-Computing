#!/usr/bin/env python3
import sys
from collections import defaultdict

def reducer():
    # Dictionary to store player-zone statistics
    player_zone_stats = defaultdict(lambda: defaultdict(lambda: {'total_shots': 0, 'total_made': 0}))

    # Read input from standard input (stdin)
    for line in sys.stdin:
        try:
            # Parse the input line
            player_name, zone, shot_result = line.strip().split(',')
            shot_result = int(shot_result)

            # Update player-zone statistics
            player_zone_stats[player_name][zone]['total_shots'] += 1
            player_zone_stats[player_name][zone]['total_made'] += shot_result
        except Exception as e:
            # Handle any errors (e.g., malformed input)
            sys.stderr.write(f"Error processing line: {line}\n")
            sys.stderr.write(f"Exception: {str(e)}\n")

    # Dictionary to store the best zone for each player
    best_zones = defaultdict(lambda: {'zone': None, 'hit_rate': -1})

    # Calculate hit rate and find the best zone for each player
    for player_name, zone_stats in player_zone_stats.items():
        for zone, stats in zone_stats.items():
            total_shots = stats['total_shots']
            total_made = stats['total_made']
            hit_rate = total_made / total_shots if total_shots > 0 else 0

            # Update the best zone for the player
            if hit_rate > best_zones[player_name]['hit_rate']:
                best_zones[player_name]['zone'] = zone
                best_zones[player_name]['hit_rate'] = hit_rate

    # Emit the best zone for each player
    for player_name, data in best_zones.items():
        zone = data['zone']
        hit_rate = data['hit_rate']
        print(f"{player_name},{zone},{hit_rate}")

if __name__ == "__main__":
    reducer()
