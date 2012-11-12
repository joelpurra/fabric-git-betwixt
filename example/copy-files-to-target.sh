#!/bin/bash

#
# Copy files from your project to a target folder for deployment.
# Modify the lines copying files below.
#

# Change to this script's folder
cd $(dirname "${0}")

TARGET="${1}"


# Check if a target directory was passed as an argument
if [[ -z "$TARGET" ]]; then
	echo "No target directory was defined" 1>&2

	# Return with a non-zero exit code to signal an error to fabric
    exit 1
fi


# Check if the target directory exists
if [[ ! -d "$TARGET" ]]; then
	echo "Could not find target directory $TARGET" 1>&2

	# Return with a non-zero exit code to signal an error to fabric
    exit 1
fi


echo "Copying files to target directory $TARGET"

### Modify these lines to make sure you copy all the right files for your deployment
cp -R a-folder-with-files "$TARGET/"
cp -R another-folder "$TARGET/"
cp one-specific-file.html "$TARGET/"
### End modifications

echo "Done copying files to target directory $TARGET"

# Return to original folder
cd - > /dev/null
