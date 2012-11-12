#!/bin/bash

#
# Wrapper file to simplify installing the right virtual environment
#

# Change to this script's folder to simplify relative paths
cd $(dirname "${0}")

virtenv=".deployment-env"

export PIP_REQUIRE_VIRTUALENV=true

# Download virtualenv into a local, hidden and ignored folder
# Could be put in a separate library directory in your project,
# or be cloned from virtualenv's github
mkdir -p .virtualenv/
cd .virtualenv/
curl https://raw.github.com/pypa/virtualenv/master/virtualenv.py > virtualenv.py
cd -


# Create virtual environment for python scripts and requirements/dependencies
python .virtualenv/virtualenv.py "$virtenv" --no-site-packages

source "$virtenv/bin/activate"

# Install betwixt
pip install --upgrade -r requirements.txt

# Return to original folder the script was run from
cd - > /dev/null