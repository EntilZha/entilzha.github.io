#!/usr/bin/env bash

set -e

pelican content -o output -s publishconf.py
ghp-import -b master -m 'Updated website' output

echo "Now run git checkout master, git push origin master, git checkout source"

