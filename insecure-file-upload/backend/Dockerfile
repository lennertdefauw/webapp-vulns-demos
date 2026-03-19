FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/uploads

# Pre-seeded "legitimate" automation scripts
RUN echo 'import platform\nprint("Host:", platform.node())\nprint("OS:", platform.system(), platform.release())\nprint("Arch:", platform.machine())\nprint("Status: all systems operational")' \
    > /app/uploads/healthcheck.py

RUN echo 'import datetime\nprint("Backup job started at", datetime.datetime.now())\nprint("Archiving logs... done (142 files, 1.2 GB)")\nprint("Uploading to offsite storage... done")\nprint("Backup completed successfully.")' \
    > /app/uploads/backup.py

RUN echo 'import os, shutil\nprint("Log rotation started...")\nprint("Rotated: /var/log/app.log -> app.log.1")\nprint("Rotated: /var/log/access.log -> access.log.1")\nprint("Freed: 2.3 GB")\nprint("Cleanup complete.")' \
    > /app/uploads/cleanup.py

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
