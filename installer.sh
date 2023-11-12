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

# Add personal bashrc settings to environment
source /root/.bashrc

# Install Miniconda
# Download the installer, run it, then remove it
curl -o $HOME/mini.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
bash $HOME/mini.sh -b -u
rm -rf $HOME/mini.sh

# Add conda to path
~/miniconda3/bin/conda init bash
echo "PATH=$PATH:/root/miniconda3/bin/" >> /root/.bashrc
PATH=$PATH:/root/miniconda3/bin/

# Source /root/.bashrc
# It's assumed that this file exists and is readable
if [[ -f /root/.bashrc ]]; then
    source /root/.bashrc
else
    echo "/root/.bashrc does not exist or is not readable"
    exit 1
fi

# Install Python 3.11 and pip
conda install -y python==3.11 pip

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
if ! command -v node >/dev/null 2>&1; then
    apt-get install -y nodejs npm
fi
if ! command -v gcc >/dev/null 2>&1; then
    apt-get install -y build-essential
fi

# Install aider for extra j00se
pip install aider-chat

# Install VueJS
npm install -g @vue/cli @vue/compiler-sfc

# Create VueJS Project
vue create --preset ./presets/vue-preset.json $PROJECT
cd $PROJECT
#cp ../presets/package.json ./package.json

#echo "export $PATH:/com.docker.devenvironments.code/klingon-auth-proxy/node_modules/.bin" >> /root/.bashrc
#PATH=$PATH:/com.docker.devenvironments.code/klingon-auth-proxy/node_modules/.bin


# Install project dependencies
npm install vue-router
npm install axios
npm install vuex
npm install vuetify
npm install bootstrap-vue

# Run NPM server
npm run serve