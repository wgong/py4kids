#!/bin/bash

# Ensure Python is run from the container's environment
# Note: AWS time is typically UTC, but we rely on the host's cron running at 1 AM EST

echo "--- Starting Batch Job Runner ---"
echo "Hostname ID: $(hostname)"
echo "Current Time (UTC/Host): $(date -u '+%Y-%m-%d %H:%M:%S')"

# Check the hour to ensure we are in the 1 AM to 4 AM window for safety 
# (although cron should control this)
CURRENT_HOUR=$(date +%H)
# Convert 1 AM EST to UTC (assuming the Docker host uses UTC or cron is configured for EST)
# 1 AM EST is 6 AM UTC / 5 AM UTC depending on DST. 
# We'll rely on the cron schedule (below) to be accurate for 1 AM EST.
# This check is mostly a safeguard.

# For simplicity, just run the Python script. The Python script handles all logic.
/usr/local/bin/python /app/batch_job.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Batch job script completed successfully."
else
    echo "Batch job script encountered an error."
fi

echo "--- Batch Job Runner Finished ---"
exit $EXIT_CODE