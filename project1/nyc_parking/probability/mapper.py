#!/usr/bin/env python3
import sys
import csv

TARGET_STREET_CODES = {"34510", "10030", "34050"}

def process_line(line):
    try:
        fields = list(csv.reader([line]))[0]  # Parse CSV row
        if len(fields) < 40:  # Ensure enough columns
            return
        
        vehicle_color = fields[33].strip().upper()  # Vehicle Color
        street_codes = {fields[9].strip(), fields[10].strip(), fields[11].strip()}  # Street Codes

        if vehicle_color == "BLACK" and TARGET_STREET_CODES.intersection(street_codes):
            print("black_vehicle\t1")  # Black vehicle received a ticket
        print("total_black_vehicles\t1")  # Count all black vehicles

    except Exception as e:
        pass  # Ignore errors in malformed lines

for line in sys.stdin:
    process_line(line)

