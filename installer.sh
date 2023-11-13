#!/bin/bash
###
### Klingon Auth Proxy Dev Environment Setup Script
###

set -e # Exit on error
set -u # Exit when it tries to use undefined variable

# Project name
PROJECT="klingon-auth-proxy"

# Add personal bashrc exports to bashrc
# This will add the line every time the script runs, consider checking if the line already exists
if ! grep -q "export AWS" /root/.bashrc; then
    cat /root/.bash_profile | grep -v "#" | grep "export AWS" >> /root/.bashrc
fi
if ! grep -q "export OPENAI" /root/.bashrc; then
    cat /root/.bash_profile | grep -v "#" | grep "export OPENAI" >> /root/.bashrc
fi
if ! grep -q "export GITHUB" /root/.bashrc; then
    cat /root/.bash_profile | grep -v "#" | grep "export GITHUB" >> /root/.bashrc
fi

# Source /root/.bashrc
# It's assumed that this file exists and is readable
if [[ -f /root/.bashrc ]]; then
    source /root/.bashrc
else
    echo "/root/.bashrc does not exist or is not readable"
    exit 1
fi

# Install apt packages
apt-get -y update; apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    git \
    gnupg-agent \
    jq \
    make \
    python3 \
    python3-pip \
    software-properties-common \
    unzip \
    wget

# Make application directory safe for git
git config --global --add safe.directory /com.docker.devenvironments.code

# Install requirements.txt
pip install -r /app/requirements.txt

# Install aider for debugging and tests    
pip install aider-chat

