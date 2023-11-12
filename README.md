# Klingon Auth Backend

## Overview
This project provides a Python-based authentication handler for NGINX, which validates user credentials against an `.htaccess` file. It's designed to be used in conjunction with NGINX's `ngx_http_auth_request_module` for custom authentication.

## Features
- Validates user credentials from NGINX against an `.htaccess` file.
- Simple HTTP server setup in Python.
- Dockerized for easy deployment and isolation.

## Prerequisites
- Docker and Docker Compose installed on your system.
- NGINX installed with `ngx_http_auth_request_module`.

## Installation

### Setting Up the Authentication Handler
1. **Clone the Repository**
   - Clone this repository to your local machine or server.
   ```bash
   git clone [REPOSITORY_URL]
   ```

2. **Docker Compose Setup**
   - Navigate to the cloned directory.
   - Ensure the `docker-compose.yml` and `Dockerfile` are present.

3. **Configure `.htaccess` File**
   - Place your `.htaccess` file in a known directory.
   - Update the `docker-compose.yml` file to mount your `.htaccess` file correctly.
     Replace `/path/to/your/local/htaccess` with the path to your `.htaccess` file.

### Configuring NGINX
1. **Update NGINX Configuration**
   - Edit your NGINX configuration file to include the authentication handler.
   - Setup a location block to forward authentication requests to the Python script.
   ```nginx
   location = /auth {
     internal;
     proxy_pass http://localhost:9111;
     proxy_set_header Content-Length "";
     proxy_set_header X-Original-URI $request_uri;
   }
   ```

## Usage

### Running the Authentication Handler
- From the project directory, run the following command to start the authentication service:
  ```bash
  docker-compose up --build
  ```

### Accessing Protected Resources
- Once NGINX and the authentication handler are running, any request to a protected location in NGINX will trigger the authentication process.
- NGINX will forward authentication requests to the Python script, which then validates credentials against the `.htaccess` file.

## Security Note
- Ensure that your `.htaccess` file and NGINX configuration are secured and not publicly accessible.
- Regularly update and monitor your NGINX and Docker installations for security patches.

## Support
For support, please open an issue in the repository, or contact the maintainer at klingon-auth-backend+david@hooton.org
