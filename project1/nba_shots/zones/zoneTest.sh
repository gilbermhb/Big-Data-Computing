#!/bin/sh

echo "Starting HDFS..."
start-dfs.sh
start-yarn.sh

echo "Checking and removing previous output directory before running the job..."
hdfs dfs -rm -r /project1/nba_shots/zoneOutput

echo "Running Hadoop Streaming job..."
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /project1/nba_shots/nba_shots.csv \
    -output /project1/nba_shots/zoneOutput \
    -mapper "python3 zoneMapper.py" \
    -reducer "python3 zoneReducer.py" \
    -file ./zoneMapper.py \
    -file ./zoneReducer.py

echo "Displaying job results..."
hdfs dfs -cat /project1/nba_shots/zoneOutput/part-00000

echo "Cleaning up old output directory..."
hdfs dfs -rm -r /project1/nba_shots/zoneOutput

echo "Stopping HDFS..."
stop-dfs.sh
stop-yarn.sh

