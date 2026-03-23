# webapp-vulns-demos
> ⚠️ **For demonstration purposes only.** This project contains intentionally vulnerable web applications. Do **not** deploy these in a production environment or expose them to the public internet.

A collection of Docker-based demos showcasing common web application vulnerabilities, intended for educational and awareness purposes.

## Vulnerabilities covered

- **CSRF** – Cross-Site Request Forgery
- **Insecure File Upload**
- **Path Traversal**
- **SQL Injection**
- **SSRF** – Server-Side Request Forgery
- **SSTI** – Server-Side Template Injection
- **XSS** – Cross-Site Scripting

## Usage

Each vulnerability has its own directory with a `start.sh` and `stop.sh` script:

```bash
cd <vulnerability-name>
./start.sh   # Starts the Docker containers
./stop.sh    # Stops the Docker containers
```

Or use `cleanup.sh` from the root to stop and remove all running demo containers at once.

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)