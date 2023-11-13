#!/bin/bash
###
### On initial boot, this script will run to set up the environment
###

# Set up environment variables if /app/environment exists
if [ -f /app/environment ]; then
    source /app/environment
fi

# For each line in /app/environment, check to see if it already exists in
# ~/.bashrc If it doesn't, add it to the end of the file
if [ -f /app/environment ]; then
    while read -r line; do
        if ! grep -q "$line" ~/.bashrc; then
            echo "$line" >> ~/.bashrc
        fi
    done < /app/environment
fi

# Add git config
git config --global user.email $MY_EMAIL
git config --global user.name $MY_NAME

# Make application directory safe for git
git config --global --add safe.directory /com.docker.devenvironments.code

# Set up git pull rebase
git config pull.rebase true