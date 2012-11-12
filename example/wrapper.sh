#!/bin/bash

#
# Wrapper file to simplify using the right virtual environment
#

# Change to this script's folder to simplify relative paths
cd $(dirname "${0}")

virtenv=".deployment-env"

# Activate the virtual deployment environment for python
source "$virtenv/bin/activate"

# Pass all script arguments to fabric
fab "$@"

# Return to original folder the script was run from
cd - > /dev/null