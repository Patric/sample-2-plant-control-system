#!/bin/bash

cd ~/sample2/rpi/scripts
# scripts to be run after system start
chmod +x start-experiment.sh
sh start-experiment.sh

LOG_FILE="$1"
# Set a default log file location if the parameter was empty, i.e. not specified.
if [ -z "$LOG_FILE" ]
then
  LOG_FILE="/var/log/testlog.txt"
fi
# Append information to the log file.
echo "----------------------------------------" >> "$LOG_FILE"
echo "System date and time: $(date '+%d/%m/%Y %H:%M:%S')" >> "$LOG_FILE"
echo "Kernel info: $(uname -rmv)" >> "$LOG_FILE"
