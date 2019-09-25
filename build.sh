#!/usr/bin/env bash

apt update
apt install -y git
apt install -y nodejs npm
npm install -g uglify-js
npm install -g babel-cli@6 babel-preset-react-app@3
pip install -r requirements.txt
git clone https://github.com/getpelican/pelican-plugins.git pelican-plugins
cd pelican-plugins
git checkout 0b9e66ee
git submodule update --recursive
cd ..
export PYTHONPATH="${PYTHONPATH}:pelican-plugins"

pelican content -o output -s publishconf.py