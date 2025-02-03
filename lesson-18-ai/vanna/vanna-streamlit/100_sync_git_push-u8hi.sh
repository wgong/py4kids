#!/bin/bash

# Define destination folder
export DEST_FOLDER="$HOME/projects/wgong/py4kids/lesson-18-ai/vanna/vanna-streamlit/"

# Check if destination folder exists
if [ ! -d "$DEST_FOLDER" ]; then
    echo "Error: Destination folder $DEST_FOLDER does not exist."
    exit 1
fi

# Copy files with verbose output
echo "Copying files to $DEST_FOLDER..."

# Copy .sh and .py files
for file in *.sh *.py; do
    if [ -e "$file" ]; then
        cp -v "$file" "$DEST_FOLDER"
    fi
done

# Copy directories
cp -rfv pages "$DEST_FOLDER"

# Copy docs from parent directory
PARENT_DIR=$(dirname "$(pwd)")
if [ -d "$PARENT_DIR/docs" ]; then
    cp -rfv "$PARENT_DIR/docs" "$DEST_FOLDER"
else
    echo "Warning: docs directory not found in parent directory."
fi

# Copy requirements.txt from parent directory
if [ -f "../requirements.txt" ]; then
    cp -v "../requirements.txt" "$DEST_FOLDER"
else
    echo "Warning: requirements.txt not found in parent directory."
fi

echo "Backup completed successfully."