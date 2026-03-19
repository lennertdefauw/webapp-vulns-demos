FROM python:3.11-slim

WORKDIR /app

# Public document root — this is what the app is "supposed" to serve
RUN mkdir -p /app/files

# Files inside the intended directory
RUN echo "Welcome to CyberCorp Document Portal!\n\nThis portal gives employees access to company documents.\nPlease only access files you are authorised to view." \
    > /app/files/welcome.txt

RUN echo "CyberCorp Document Portal — README\n\nAvailable documents:\n  - welcome.txt\n  - hr-policy.txt\n  - it-guidelines.txt\n\nContact the IT department for access issues." \
    > /app/files/readme.txt

RUN echo "CyberCorp HR Policy v3.1\n\nSection 1 — Code of Conduct\nAll employees must adhere to the company code of conduct...\n\nSection 2 — Remote Work\nEmployees may work remotely up to 3 days per week..." \
    > /app/files/hr-policy.txt

RUN echo "IT Security Guidelines v2.0\n\nAll systems must use MFA.\nPasswords must be rotated every 90 days.\nReport incidents to security@cybercorp.internal." \
    > /app/files/it-guidelines.txt

# Files OUTSIDE the intended directory — should never be reachable
RUN mkdir -p /app/secret
RUN echo "[!] CONFIDENTIAL — DO NOT DISTRIBUTE\n\nAdmin Portal: https://admin.cybercorp.internal\nUsername:      sysadmin\nPassword:      C0rp@dm!n2024!\nAPI Key:       sk-cybercorp-4f8a2b1c9d3e7f6a\nDB Root PW:    Sup3rS3cr3tDB#99" \
    > /app/secret/credentials.txt

RUN mkdir -p /app/config
RUN echo "[database]\nhost     = 10.0.0.5\nport     = 3306\nname     = cybercorp_prod\nuser     = app_user\npassword = Pr0d_DB_p@ss!\n\n[cache]\nhost     = 10.0.0.6\nport     = 6379\npassword = r3d!sS3cr3t" \
    > /app/config/database.conf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
