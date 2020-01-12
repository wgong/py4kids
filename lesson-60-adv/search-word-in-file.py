
import re
import argparse

"""
$ python search-word-in-file.py parser search-word-in-file.py
"""
def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('word', help='specify word to search for')
    parser.add_argument('fname', help='specify file to search')
    args = parser.parse_args()

    searchFile = open(args.fname)
    lineNum = 0
    
    for line in searchFile.readlines():
        line = line.strip('\n\r')
        lineNum += 1
        searchResult = re.search(args.word, line, re.M|re.I)
        if searchResult:
           print(str(lineNum) + ': ' + line)


if __name__ == '__main__':
    Main()
