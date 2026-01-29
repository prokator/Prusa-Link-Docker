# Filename: Dockerfile
# ALLOWS OVERRIDING THE BASE IMAGE REPO
ARG BASE_IMAGE=prusalink-base:latest
FROM ${BASE_IMAGE}

WORKDIR /app

# Copy the entire repository
COPY . .

# Install the Python application
RUN pip install .

# Create configuration directory
RUN mkdir -p /etc/prusalink

EXPOSE 8080

CMD ["prusalink", "-f"]