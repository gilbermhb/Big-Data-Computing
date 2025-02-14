#!/bin/sh

# Validate input arguments
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "No time range provided. Defaulting to full day (00:00 - 24:00)."
    startHour="00"
    endHour="24"
else
    startHour=$1
    endHour=$2

    # Ensure start_hour and end_hour are valid numbers between 00-23
    if ! [[ "$startHour" =~ ^[0-9]{1,2}$ ]] || ! [[ "$endHour" =~ ^[0-9]{1,2}$ ]]; then
        echo "Error: Start and end hour must be numeric (00-23)."
        exit 1
    fi

    if [ "$startHour" -lt 0 ] || [ "$startHour" -gt 23 ] || [ "$endHour" -lt 0 ] || [ "$endHour" -gt 24 ]; then
        echo "Error: Hours must be in range 00-23."
        exit 1
    fi

    if [ "$startHour" -ge "$endHour" ]; then
        echo "Error: Start hour must be less than end hour."
        exit 1
    fi
fi

# Start Hadoop
../../start.sh

# Cleanup previous runs
/usr/local/hadoop/bin/hdfs dfs -rm -r /lab1/input/ > /dev/null 2>&1
/usr/local/hadoop/bin/hdfs dfs -rm -r /lab1/output/ > /dev/null 2>&1
/usr/local/hadoop/bin/hdfs dfs -mkdir -p /lab1/input/
/usr/local/hadoop/bin/hdfs dfs -copyFromLocal ../../mapreduce-test-data/access.log /lab1/input/

# Run Hadoop MapReduce job
/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
-file ../../mapreduce-test-python/lab1/mapper.py -mapper ../../mapreduce-test-python/lab1/mapper.py \
-file ../../mapreduce-test-python/lab1/reducer.py -reducer ../../mapreduce-test-python/lab1/reducer.py \
-input /lab1/input/* -output /lab1/output/

# Check if output exists before attempting to process
if /usr/local/hadoop/bin/hdfs dfs -test -e /lab1/output/part-00000; then
    echo "Processing results for time range $startHour:00 - $endHour:00..."
    /usr/local/hadoop/bin/hdfs dfs -cat /lab1/output/part-00000 | awk -v start="$startHour" -v end="$endHour" '
    BEGIN { FS="\t" }
    {
        split($1, time, ":");
        if (time[1] >= start && time[1] <= end) {
            print $0;
        }
    }'
else
    echo "Error: No output found. Hadoop job may have failed."
fi

# Cleanup output
/usr/local/hadoop/bin/hdfs dfs -rm -r /lab1/input/ > /dev/null 2>&1
/usr/local/hadoop/bin/hdfs dfs -rm -r /lab1/output/ > /dev/null 2>&1

# Stop Hadoop
../../stop.sh
