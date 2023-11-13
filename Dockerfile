###
### Klingon Auth Proxy Dockerfile
###
# Use the official Python image.
FROM python:3.9-slim

# Copy local code to the container image.
WORKDIR /app
COPY . /app

# Install production dependencies.
RUN bash /app/installer.sh

# Run the web service on container startup.
CMD ["python", "/app/src/main.py"]
