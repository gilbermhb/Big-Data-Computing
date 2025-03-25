#!/usr/bin/env python3
import sys
import csv

def mapper():
    # Read input from standard input (stdin)
    reader = csv.reader(sys.stdin, delimiter=',')  # Parse CSV input
    next(reader, None)  # Skip the header row

    for row in reader:
        try:
            # Extract relevant fields
            player_name = row[19]  # Assuming player_name is the 20th column
            defender_name = row[14]  # Assuming CLOSEST_DEFENDER is the 15th column
            shot_result = 1 if row[13] == 'made' else 0  # Assuming SHOT_RESULT is the 14th column

            # Emit key-value pairs (use a different delimiter)
            print(f"{player_name}|{defender_name}|{shot_result}|1")
        except Exception as e:
            # Handle any errors (e.g., missing fields or malformed input)
            sys.stderr.write(f"Error processing row: {row}\n")
            sys.stderr.write(f"Exception: {str(e)}\n")

if __name__ == "__main__":
    mapper()
