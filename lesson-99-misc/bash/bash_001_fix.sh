#!/bin/bash

# Define directory list using readarray
readarray -t directories <<EOF
directory1
directory2
EOF

# Access elements in the array (optional)
for dir in "${directories[@]}"; do
  echo "Directory: $dir"
done
