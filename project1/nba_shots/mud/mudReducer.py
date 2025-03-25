#!/usr/bin/env python3e
import sys
from collections import defaultdict

def reducer():
    # Dictionary to store player-defender statistics
    player_defender_stats = defaultdict(lambda: {'total_shots': 0, 'total_made': 0})

    # Read input from standard input (stdin)
    for line in sys.stdin:
        try:
            # Parse the input line (use the same delimiter as the mapper)
            player_name, defender_name, shot_result, count = line.strip().split('|')
            shot_result = int(shot_result)
            count = int(count)

            # Update player-defender statistics
            key = (player_name, defender_name)
            player_defender_stats[key]['total_shots'] += count
            player_defender_stats[key]['total_made'] += shot_result
        except Exception as e:
            # Handle any errors (e.g., malformed input)
            sys.stderr.write(f"Error processing line: {line}\n")
            sys.stderr.write(f"Exception: {str(e)}\n")

    # Dictionary to store the most unwanted defender for each player
    most_unwanted_defenders = defaultdict(lambda: {'defender': None, 'fear_score': -1})

    # Calculate fear score and find the most unwanted defender for each player
    for (player_name, defender_name), stats in player_defender_stats.items():
        total_shots = stats['total_shots']
        total_made = stats['total_made']
        fear_score = total_made / total_shots if total_shots > 0 else 0

        # Update the most unwanted defender for the player
        if fear_score > most_unwanted_defenders[player_name]['fear_score']:
            most_unwanted_defenders[player_name]['defender'] = defender_name
            most_unwanted_defenders[player_name]['fear_score'] = fear_score

    # Emit the most unwanted defender for each player
    for player_name, data in most_unwanted_defenders.items():
        defender_name = data['defender']
        fear_score = data['fear_score']
        print(f"{player_name}|{defender_name}|{fear_score}")

if __name__ == "__main__":
    reducer()