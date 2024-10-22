https://www.kaggle.com/datasets/mylesoneill/warcraft-avatar-history?resource=download&select=wowah_data.csv


https://github.com/myles-oneill/WoWAH-parser

```
# Forked and Updated by Myles O'Neill May 2016 to collect more information from the original files

# Nov, 2013 (orig Sept 2013).
# This file will (hopefully) read all the little WoW AH files and make a csv.
# One file to unite them all! (It is like 3.5 GB of text.)
# Needs to:
# Read directory and file name structure so I don't have to type it in manually.
# Make that a data structure of some sort, easy to read so the program can scan through it.
# Writes to a CSV.

# Data:  http://mmnet.iis.sinica.edu.tw/dl/wowah/


# PACKAGES
import csv
import re
import os           # This is for os.listdir
import os.path      # This is for the other dir stuff.
import string       # Maybe for directory name cycling etc.
import time			# For timing how long it takes.

# VARIABLES
max_char = 0		# Tracks char ID for error testing.
max_guild = 0		# Tracks guild ID for error testing.
mfc = 0				# Tracks how many little files were counted.
write_data_loc = '~/wowah/output/'       	     						# Adjust to your dir as needed.
write_data_file = 'wowah_data.csv'
write_data_filename = write_data_loc + write_data_file
the_dir = '~/wowah/WoWAH/'								# This is where the WoWAH folders are located, adjust as needed. Have them in their own subdir.

#REGEX
line_re = re.compile(r'^.*"[\d+],\s(.*),\s?(\d*),\s?(\d*),\s?(\d*),\s?(\d*),\s?([A-Z].*),\s?([A-Z].*),\s?([A-Z].*),\s?([A-Z].*)".*$')
#                          dummy   time1   seq2    3char   4guild    5level     6race              7charclass       8zone

# REGEX NOTES
# groups: 1=timestamp, 3=avatarID, 4=guild.
# [1] = "0, 03/30/06 23:59:49, 1,10772, , 1, Orc, Warrior, Orgrimmar, , 0",
#       "0, 01/10/09 00:03:50, 1,55517, , 3, Orc, Warlock, Orgrimmar, WARLOCK, 0", -- [1]
#    	"0, 01/10/09 00:04:10, 5,4002,1, 75, Orc, Hunter, Zul'Gurub, HUNTER, 0", -- [26]
#       "0, 01/10/09 00:04:10, 5,78122,342, 80, Orc, Hunter, The Storm Peaks, HUNTER, 0", -- [32]
#   	"0, 01/10/09 00:08:04, 51,64635,161, 80, Blood Elf, Paladin, The Obsidian Sanctum, PALADIN, 0", -- [447]
# dummy, query time, query sequence number, avatar ID, guild, level, race, class, zone, dummy, dummy



# FUNCTIONS

def get_subdirs(the_folder):
    this_list = []
    this_list = os.listdir(the_folder)
    print 'From get_subdirs, a list is: ', this_list      # Printing for error control.
    for item in this_list:
        if item.startswith('.'):
            this_list.remove(item)
    return(this_list)
# End of get_subdirs
# '.DS_Store'


def get_file_list(the_folder):				# Yes these two are the same, just diff names.
    this_list = []
    this_list = os.listdir(the_folder)
    for item in this_list:
        if item.startswith('.'):
            this_list.remove(item)
    return(this_list)
# End of get_file_list


def parse_and_write(file, output_file):
    for line in file:                           # Oh the first "line" is a hard return???
#       print 'A line is: ', line
        data = line_re.match(line)
        if data is not(None):
            timestamp = data.group(1)
            char = data.group(3)
            level = data.group(5)
            race = data.group(6)
            charclass = data.group(7)
            zone = data.group(8)

            if data.group(4) is not(''):
                guild = data.group(4)
            else:
                guild = '-1'   # Note there are some missing values, i.e. errant -1.
            print timestamp    # This is so you can keep track of where it is. Max Jan 2009 IIRC.

            new_line = char + ',' + level + ',' + race + ',' + charclass + ',' + zone +  ',' + guild + ',' + timestamp + '\n'
            output_file.write(new_line)
                
        else:
            print "Didn't match the regex."

# End of parse_and_write
# Note the two diff formats they use in the files, it changes partway through:
# [1] = "0, 03/30/06 23:59:49, 1,10772, , 1, Orc, Warrior, Orgrimmar, , 0",
#       "0, 01/10/09 00:03:50, 1,55517, , 3, Orc, Warlock, Orgrimmar, WARLOCK, 0", -- [1]
# dummy, query time, query sequence number, avatar ID, guild, level, race, class, zone, dummy, dummy


def read_tree(output_file):
    global the_dir
    months_folders = get_subdirs(the_dir)		# This is why the subdirs should be in their own location that you set in the vars section up top.
    for folder in months_folders:                                   # Run isdir(dir) first, try/except. Make sure no funny folders/dirs.
        folder = the_dir + folder                                   # Expands the folder name to the long version.
        day_folders = get_subdirs(folder)
        for day_folder in day_folders:
            day_folder = folder + '/' + day_folder
            file_list = get_file_list(day_folder)
            for file in file_list:
                try:
                    file = day_folder + '/' + file
                    with open(file, 'r') as f:
                        this_file = f.readlines()                          # Should read the whole file as a string?
                        parse_and_write(this_file, output_file)
                except IOError:
                    print 'Error opening hoped for data-text file,', str(file), ', reason: ', IOError
# End of read_tree


def main():	
    #open write file here
    output_file = open(write_data_filename, 'a')    # 'a' is very important, it appends the new data to the big file. 
    fieldnames = ('char, level, race, charclass, zone, guild, timestamp\n')
    output_file.write(fieldnames)
    start_time = time.time()
    read_tree(output_file)
    #close write file here
    output_file.close()
    spent_time = time.time() - start_time
    mins_spent = int(spent_time / 60)
    secs_remainder = int(spent_time % 60)
    print 'Time of process: ', mins_spent, ':', secs_remainder     # 13m:42s on iMac. Also 14m:39s another time.
    
#    print 'Files scanned (or tried), ', mfc     # 138,084
#    print 'Max Chars: ', max_char               # They say 91,065 ">= 1" but it starts at 0, my count says: 91064 + 1 = 91,065.
#    print 'Max Guilds: ', max_guild             # They say "An integer within [1, 513]" but no since they start at 0. 512 + 1 = 513.
# End of main


# Main call

main()
```