#!/bin/bash

############################################
## this script does two-way rsync
## provided by Google Gemini
## revised by me 

# Usage: 
#   $ bash usb_rsync.sh 
############################################
# Exit code (set to 1 initially, indicating failure)
exit_code=1

# set 1 for dry_run mode
dry_run_mode=0

if [ $dry_run_mode -eq 1 ]; then
  echo "====================================="
  echo "        Perform dry-run"
  echo "====================================="
fi


skip_char="#"
# Function to check if a string starts with a character after trimming spaces
function is_string_trimmed_start_with() {
  local string_var="$1"     # Function argument for the string to check
  local start_char="$2"     # Function argument for the starting character

  # Trim leading and trailing spaces from the string
  trimmed_string="${string_var}"
  trimmed_string=${trimmed_string#" "}  # Remove leading spaces
  trimmed_string=${trimmed_string%" "}  # Remove trailing spaces

  # Check if the trimmed string starts with the specified character
  if [[ "${trimmed_string:0:1}" == "$start_char" ]]; then
    return 1  # Return true if it starts with the character
  else
    return 0 # Return false otherwise
  fi
}


# Define directory list using readarray
# fixed by Claude
readarray -t folders_to_sync <<EOF
toolbox
# vanna
zilab
EOF

source_dir_root="/home/gongai/projects/1_Biz"
# change for different USB drive
USB_DRIVE_NAME="USB321FD"

# Define the mount point for your USB flash drive (replace with your actual path)
usb_mountpoint="/media/gongai/$USB_DRIVE_NAME"

dest_dir_root="$usb_mountpoint/1_Biz"
# Check if destination directory exists
if [ ! -d "$dest_dir_root" ]; then
  # Create directory if it doesn't exist
  mkdir -p "$dest_dir_root"
fi

# Function to check if the USB drive is mounted
function is_usb_mounted() {
  if [ -e "$usb_mountpoint" ]; then
    exit_code=0  # Update exit code to 0 if mounted
    return 0      # Return success (0)
  else
    return 1      # Return failure (1)
  fi
}


# Check if USB drive is mounted
is_usb_mounted

# Exit if USB drive is not mounted
if [ $exit_code -eq 1 ]; then
  echo "Error: USB flash drive not mounted at '$usb_mountpoint'"
  exit $exit_code
fi

# Loop through each folder in the list
for folder in "${folders_to_sync[@]}"; do
  is_string_trimmed_start_with "$folder" "$skip_char"
  to_skip=$?
  if [[ "$to_skip" -eq 1 ]]; then
    echo "========================"
    echo "Skipping folder: $folder"
    continue
  fi


  source_dir="$source_dir_root/$folder"  # Replace with actual source path
  dest_dir="$dest_dir_root/$folder"      # Replace with actual destination path (USB)

  # Sync from source to USB (newer files)
  echo "Syncing '$source_dir' to '$dest_dir' (source -> USB)"
  if [ $dry_run_mode -eq 1 ]; then
    rsync -avutn --inplace "$source_dir/" "$dest_dir/"
  else
    rsync -avut --inplace "$source_dir/" "$dest_dir/"
  fi 

  # sync in reverse direction only if destination directory exists
  if [ -d "$dest_dir" ]; then
    # Sync from USB to source (newer files)
    echo "Syncing '$dest_dir' to '$source_dir' (USB -> source)"
    if [ $dry_run_mode -eq 1 ]; then
        rsync -avutn --inplace "$dest_dir/" "$source_dir/"
    else
        rsync -avut --inplace "$dest_dir/" "$source_dir/"
    fi 

  fi

done

echo "Sync completed!"

exit $exit_code
