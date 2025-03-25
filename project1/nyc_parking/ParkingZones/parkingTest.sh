#!/bin/sh

echo "Starting HDFS..."
start-dfs.sh
start-yarn.sh

echo "Checking and removing previous output directory before running the job..."
hdfs dfs -rm -r /project1/nyc_parking/ParkingZones/OutputParkingZones

echo "Running Hadoop Streaming job..."
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /project1/nyc_parking/nyc_parking.csv \
    -output /project1/nyc_parking/ParkingZones/OutputParkingZones \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -file ./mapper.py \
    -file ./reducer.py

echo "Displaying job results..."
hdfs dfs -cat /project1/nyc_parking/ParkingZones/OutputParkingZones/part-*

echo "Cleaning up old output directory..."
hdfs dfs -rm -r /project1/nyc_parking/ParkingZones/OutputParkingZones

echo "Stopping HDFS..."
stop-dfs.sh
stop-yarn.sh

