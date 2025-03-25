#!/usr/bin/env python3
import sys
import csv

TARGET_TIME_START = 930  # 09:30 AM
TARGET_TIME_END = 1030  # 10:30 AM

def parse_violation_time(time_str):
    try:
        time_str = time_str.strip().upper()
        if not time_str:
            return None
        if time_str[-1] in ("A", "P"):
            time_num = int(time_str[:-1])
            if time_str[-1] == "P" and time_num < 1200:
                time_num += 1200
        else:
            time_num = int(time_str)
        return time_num
    except:
        return None

for line in sys.stdin:
    try:
        fields = list(csv.reader([line]))[0]
        if len(fields) < 40:
            continue

        violation_time = parse_violation_time(fields[19].strip())
        if violation_time is None:
            continue

        street_codes = [fields[9].strip(), fields[10].strip(), fields[11].strip()]
        if TARGET_TIME_START <= violation_time <= TARGET_TIME_END:
            for street_code in street_codes:
                if street_code.isdigit():
                    print(f"{street_code}\t1")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)

