#!/bin/bash

# Define temporary file for directory list
temp_file=$(mktemp)

# Write directory list to temporary file
echo "directory1" >> "$temp_file"
echo "directory2" >> "$temp_file"

# Read directories line by line from the temporary file
directories=( )
while IFS= read -r line; do
  directories+=("$line")
done < "$temp_file"

# Clean up the temporary file
rm "$temp_file"

# Access elements in the array (optional)
for dir in "${directories[@]}"; do
  echo "Directory: $dir"
done

