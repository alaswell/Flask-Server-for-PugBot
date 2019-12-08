#!/bin/bash

echo "Initiating run server script"

if pgrep -f 'flaskServer.py'
then
	echo "    Flask is currently running"
	echo "    Stopping the existing process first. This action has been logged"
	nows=$(date +"%m%d%Y.%H%M%S")
	echo "A force stop has occurred at $nows" >> logs/force_stops
	`kill $(pgrep -f 'flaskServer.py')`
fi

echo "    Reading and incrementing the debug counter"
typeset -i number_of_restarts=$(head -n 1 flaskServer.out.log)
number_of_restarts=$((number_of_restarts + 1))

echo "    Timestamping and saving the old log files"
now=$(date +"%m%d%Y.%H%M%S")
mv flaskServer.err.log logs/flaskServer.err.$now
mv flaskServer.out.log logs/flaskServer.out.$now

echo "    Creating a new output file and adding the debug counter to it"
echo "$number_of_restarts" > flaskServer.out.log

echo "    Starting the flask server"
python3 flaskServer.py >> flaskServer.out.log 2>> flaskServer.err.log < /dev/null &

echo "The run server script is complete"
