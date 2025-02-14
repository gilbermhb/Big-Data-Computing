#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict


#========================================================================================
#  Creating a dictionary to store the count of IP addresses per hour
#========================================================================================

ipCount = defaultdict(lambda: defaultdict(int))


#========================================================================================
# Reading input from the mapper and counting the occurrences of each IP address per hour
#========================================================================================
for line in sys.stdin:
    line = line.strip()
    try:
        hour, ip, count = line.split('\t')
        count = int(count)
        ipCount[hour][ip] += count
    except ValueError:
        pass # Handle the case where the line does not split into exactly three parts

#========================================================================================
# Sorting the IP addresses for each hour and printing the top 3
#========================================================================================
for hour in sorted(ipCount.keys()):
    ipSorted = sorted(ipCount[hour].items(), key=lambda x: x[1], reverse=True)[:3] # Sorting in descending order and taking the top 3
    for ip, count in ipSorted:
        print(f"{hour}\t{ip}\t{count}")
