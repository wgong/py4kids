#!/bin/bash
skip_char="#"

# Function to check if a string starts with a character after trimming spaces
function is_string_trimmed_start_with() {
  local string_var="$1"     # Function argument for the string to check
  local skip_char="$2"     # Function argument for the starting character

  # Trim leading and trailing spaces from the string
  trimmed_string="${string_var}"
  trimmed_string=${trimmed_string#" "}  # Remove leading spaces
  trimmed_string=${trimmed_string%" "}  # Remove trailing spaces

  # Check if the trimmed string starts with the specified character
  if [[ "${trimmed_string:0:1}" == "$skip_char" ]]; then
    return 1  # Return true if it starts with the character
  else
    return 0 # Return false otherwise
  fi
}

# Example usage
# Define directory list using readarray
readarray -t folders_to_sync <<EOF
toolbox
# vanna
# zilab
EOF



# Print the to_skip
for folder in "${folders_to_sync[@]}"; do
  is_string_trimmed_start_with "$folder" "$skip_char"
  to_skip=$?
  echo "Result: $to_skip"
  if [[ "$to_skip" -eq 1 ]]; then
    echo "========================"
    echo "Skipping: $folder"
    continue
  else 
    echo "Processing: $folder"
    echo "Doing work in : $folder"
  fi
done
