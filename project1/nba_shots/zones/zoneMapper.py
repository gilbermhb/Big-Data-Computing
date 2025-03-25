#!/usr/bin/env python3
import sys
import csv

#Define a quantile-based comfortable zones
def classify_zone(shot_dist, def_dist, shot_clock):
    if shot_dist <= 4.7 and def_dist <= 2.3 and shot_clock <= 8.2:
        return "Zone 1"  # Close-range, highly contested, rushed shot
    elif shot_dist <= 13.7 and def_dist <= 3.7 and shot_clock <= 12.3:
        return "Zone 2"  # Mid-range, moderately contested, normal shot
    elif shot_dist <= 22.5 and def_dist <= 5.3 and shot_clock <= 16.7:
        return "Zone 3"  # Long mid-range, lightly contested, comfortable shot
    else:
        return "Zone 4"  # Three-point/deep shot, open shot

def mapper():
    # Read input from standard input (stdin)
    reader = csv.reader(sys.stdin, delimiter=',')  # Parse CSV input
    next(reader, None)  # Skip the header row

    for row in reader:
        try:
            # Extract relevant fields
            player_name = row[19]  # Assuming player_name is the 20th column
            shot_dist = float(row[9])  # Assuming SHOT_DIST is the 10th column
            close_def_dist = float(row[15])  # Assuming CLOSE_DEF_DIST is the 16th column
            shot_clock = float(row[8]) if row[8] else 0  # Assuming SHOT_CLOCK is the 9th column (handle missing values)
            shot_result = 1 if row[13] == 'made' else 0  # Assuming SHOT_RESULT is the 14th column

            # Classify the shot into a zone
            zone = classify_zone(shot_dist, close_def_dist, shot_clock)

            # Emit key-value pairs
            print(f"{player_name},{zone},{shot_result}")
        except Exception as e:
            # Handle any errors (e.g., missing fields or malformed input)
            sys.stderr.write(f"Error processing row: {row}\n")
            sys.stderr.write(f"Exception: {str(e)}\n")

if __name__ == "__main__":
    mapper()
