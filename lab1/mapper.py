#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys

#======================================================================
# Defining the regular expression pattern to match the log lines
#======================================================================
pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\d{4}:(?P<hour>\d{2}):\d{2}.*?')

#======================================================================
# Formatting the output to display the hour and IP address
#======================================================================
for line in sys.stdin:
    match = pattern.search(line)
    if match:
        ipAddress = match.group('ip')
        hour = match.group('hour')
        print(f"{hour}:00\t{ipAddress}\t1") # Output format: hour:00\tIP address\t1 where 1 is the count



