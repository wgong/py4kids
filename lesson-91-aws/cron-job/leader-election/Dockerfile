# ... (Your existing Dockerfile content) ...

# Install cron and other necessary tools
RUN apt-get update && apt-get install -y \
    cron \
    # Install the AWS CLI if you prefer to use that instead of Boto3 
    # or need other tools
    # awscli \ 
    # python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the scripts into the container
WORKDIR /app
COPY batch_job.py /app/
COPY run_batch.sh /app/
RUN chmod +x /app/run_batch.sh

# --- CRONTAB SETUP ---
# Cron schedule: 1 AM EST daily. 
# You need to ensure the container's environment respects the timezone setting (TZ).
# 0 1 * * * command_to_run 

# Set the timezone to EST (or America/New_York) to ensure 1 AM is 1 AM local time
ENV TZ="America/New_York"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set up the crontab file to run the bash script daily at 1 AM (0 1 * * *)
# Note: The output is redirected to a log file.
RUN (crontab -l 2>/dev/null; echo "0 1 * * * /app/run_batch.sh >> /var/log/cron.log 2>&1") | crontab -

# To start cron when the container starts, you must change your entrypoint/command.
# Replace your current CMD/ENTRYPOINT with a script that starts cron and your Flask app.
# Example startup script (start_all.sh):
# #!/bin/bash
# cron -f &
# exec gunicorn ... # (Your original Flask startup command)

# Final Docker CMD/ENTRYPOINT:
CMD ["/bin/bash", "-c", "cron && tail -f /var/log/cron.log & exec gunicorn -b 0.0.0.0:5000 'app:app'"] 
# Adjust 'gunicorn -b 0.0.0.0:5000 'app:app'' to your actual Flask startup command.