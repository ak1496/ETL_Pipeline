# Use the official Superset image as the base
FROM apache/superset:3.0.0

# Switch to root user to install system packages
USER root

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Switch back to the default Superset user (check the base image's Dockerfile if unsure, but this is common)
USER superset
