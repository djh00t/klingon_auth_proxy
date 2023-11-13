#!/bin/bash
###
### On initial boot, this script will run to set up the environment
###

# Set up environment variables if /app/environment exists
if [ -f /app/environment ]; then
    source /app/environment
fi
  
# Add git config
git config --global user.email $MY_EMAIL
git config --global user.name $MY_NAME

# Make application directory safe for git
git config --global --add safe.directory /com.docker.devenvironments.code

# Set up git pull rebase
git config pull.rebase true