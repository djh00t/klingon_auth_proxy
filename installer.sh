#!/bin/bash
###
### Klingon Auth Proxy Dev Environment Setup Script
###
PROJECT="klingon-auth-proxy"
# Source personal bash profile
source /root/.bash_profile 
# Add personal bashrc to bashrc
echo "source /root/.bash_profile" >> /root/.bashrc
# Install Miniconda
curl -o mini.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh;bash mini.sh -b -p $HOME/miniconda;rm -rf mini.sh
# Source /root/.bashrc
source /root/.bashrc
# Install Python 3.11 and pip
conda install python==3.11 pip
# Install NodeJS and NPM
apt-get update; apt-get -y dist-upgrade; sudo apt-get install -y nodejs npm

# Install aider for extra j00se
pip install aider-chat

# Install VueJS
npm install -g @vue/cli

# Create VueJS Project
vue create $PROJECT
cd $PROJECT

# NPM Install
npm install

# Update VueJS Project
npm audit fix --force

# run NPM server
npm run serve

