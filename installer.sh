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
cat /root/.bash_profile | grep -v "#" | grep "export AWS" >> /root/.bashrc
cat /root/.bash_profile | grep -v "#" | grep "export OPENAI" >> /root/.bashrc
cat /root/.bash_profile | grep -v "#" | grep "export GITHUB" >> /root/.bashrc

# Add personal bashrc settings to environment
source /root/.bashrc

# Install Miniconda
# Download the installer, run it, then remove it
curl -o $HOME/mini.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
bash $HOME/mini.sh -b -u
rm -rf $HOME/mini.sh

# Source /root/.bashrc
# It's assumed that this file exists and is readable
if [[ -f /root/.bashrc ]]; then
    source /root/.bashrc
else
    echo "/root/.bashrc does not exist or is not readable"
    exit 1
fi

# Install Python 3.11 and pip
conda install python==3.11 pip

# Source /root/.bashrc
# It's assumed that this file exists and is readable
if [[ -f /root/.bashrc ]]; then
    source /root/.bashrc
else
    echo "/root/.bashrc does not exist or is not readable"
    exit 1
fi

# Update the system and install NodeJS and NPM
apt-get update
apt-get -y dist-upgrade
apt-get install -y nodejs npm

# Install aider for extra j00se
pip install aider-chat

# Install VueJS
npm install -g @vue/cli

# Create VueJS Project
vue create $PROJECT
cd $PROJECT

# Install project dependencies
npm install

# Update VueJS Project
npm audit fix --force

# Run NPM server
npm run serve