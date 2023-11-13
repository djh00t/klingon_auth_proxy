#!/bin/bash
###
### Klingon Auth Proxy Dev Environment Setup Script
###

set -e # Exit on error
set -u # Exit when it tries to use undefined variable

# Project name
PROJECT="klingon-auth-proxy"

# Make application directory safe for git
git config --global --add safe.directory /com.docker.devenvironments.code

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

# Install aider for extra j00se
pip install aider-chat

