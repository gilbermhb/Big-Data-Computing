#!/bin/sh

echo "Starting HDFS..."
start-dfs.sh
start-yarn.sh

echo "Fetching latest Mapper and Reducer from HDFS..."
hdfs dfs -get /project1/nba_shots/mudMapper.py .
hdfs dfs -get /project1/nba_shots/mudReducer.py .

echo "Ensuring Mapper and Reducer are executable..."
chmod +x mudMapper.py mudReducer.py

echo "Checking and removing previous output directory before running the job..."
hdfs dfs -rm -r /project1/nba_shots/mudOutput

echo "Running Hadoop Streaming job..."
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /project1/nba_shots/nba_shots.csv \
    -output /project1/nba_shots/mudOutput \
    -mapper "python3 mudMapper.py" \
    -reducer "python3 mudReducer.py" \
    -file ./mudMapper.py \
    -file ./mudReducer.py

echo "Displaying job results..."
hdfs dfs -cat /project1/nba_shots/mudOutput/part-00000

echo "Cleaning up old output directory..."
hdfs dfs -rm -r /project1/nba_shots/mudOutput

echo "Stopping HDFS..."
stop-dfs.sh
stop-yarn.sh

