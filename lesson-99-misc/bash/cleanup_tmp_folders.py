#!/usr/bin/env python
# coding: utf-8

import os
import re

def remove_folders_by_pattern(start_dir, pattern="[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}", rm_flag=False):
  """
  Walks a folder structure starting from 'start_dir' and removes folders 
  whose names match the provided 'pattern' (regular expression).

  Args:
    start_dir: The directory path to start walking from.
    pattern: A regular expression string to match folder names.
  """
  pattern_regex = re.compile(pattern)
  for dirpath, dirnames, filenames in os.walk(start_dir):
    for dirname in dirnames:
      if pattern_regex.match(dirname):
        full_path = os.path.join(dirpath, dirname)
        # Print the folder to be removed for confirmation (optional)
        print(f"Removing directory: {full_path}")
        # Uncomment the following line to actually remove the folder
        if rm_flag:
            # os.rmdir(full_path)
            try:
                remove_folder_tree(full_path)
            except OSError as e:
                print(f"Error deleting {full_path}: {e}")

def remove_folder_tree(path):
  """
  Recursively removes a folder and its entire contents.

  Args:
    path: The directory path to remove.

  **Warning:** This function permanently deletes files and folders. 
             Use with caution and ensure you have backups.
  """
  if os.path.isfile(path):
    os.remove(path)  # Remove a file if it's the target
  elif os.path.isdir(path):
    for item in os.listdir(path):
      itempath = os.path.join(path, item)
      remove_folder_tree(itempath)  # Recursive call
    os.rmdir(path)  # Remove the empty directory after subcontents are gone

if __name__ == "__main__":
    RM_FLAG = True # False
    # clean up tmp folder like "820fb7ca-dc6f-40d6-8657-268ed85b929f"
    remove_folders_by_pattern(".", rm_flag=RM_FLAG)

    # clean up tmp jupyter notebook folder
    pattern = "\.ipynb_checkpoints"
    remove_folders_by_pattern(".", pattern=pattern, rm_flag=RM_FLAG)

