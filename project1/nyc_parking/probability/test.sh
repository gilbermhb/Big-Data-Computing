#!/bin/sh

echo "Starting HDFS..."
start-dfs.sh
start-yarn.sh

echo "Fetching latest Mapper and Reducer from HDFS..."
hdfs dfs -get /project1/nyc_parking/Probability/mapper.py .
hdfs dfs -get /project1/nyc_parking/Probability/reducer.py .

echo "Ensuring Mapper and Reducer are executable..."
chmod +x mapper.py reducer.py

echo "Checking and removing previous output directory before running the job..."
hdfs dfs -rm -r /project1/nyc_parking/Probability/OutputBlackVehicle

echo "Running Hadoop Streaming job..."
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /project1/nyc_parking/nyc_parking.csv \
    -output /project1/nyc_parking/Probability/OutputBlackVehicle \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -file ./mapper.py \
    -file ./reducer.py

echo "Displaying job results..."
hdfs dfs -cat /project1/nyc_parking/Probability/OutputBlackVehicle/part-*

echo "Cleaning up old output directory..."
hdfs dfs -rm -r /project1/nyc_parking/Probability/OutputBlackVehicle

echo "Stopping HDFS..."
stop-dfs.sh
stop-yarn.sh

