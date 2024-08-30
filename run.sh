#!/bin/bash

while true
do
    python3 main.py
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "Program exited normally with code $exit_code. Exiting script."
        break  # exit the bash script
    else
        echo "Program crashed with exit code $exit_code. Restarting..." >&2
    fi

    sleep 1  
done
#need to change the execution path to set relative path
