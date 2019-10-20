#!/usr/bin/python3

# Parses CSS files in the css directory and generates information on the css color usage

import os
import sys
import json

import cssparse

colorDictionary = {}

OUTPUT = "results.json"

DIRECTORY = "css"

def main():
    print("Parsing CSS files in css directory")
    traverse()
    # Testing Parsing
    # f = open("test.css")
    # parse(f.read())
    # f.close()

    genReport()


# Traverses a directory (only 1 level)
def traverse():
    global DIRECTORY
    if not os.path.exists(DIRECTORY):
        raise Exception("Directory " + DIRECTORY + " does not exist!")
    if os.path.isdir(DIRECTORY):
        with os.scandir(DIRECTORY) as iter:
            for entry in iter:
                if entry.is_file():
                    print("Opening File ", entry.path)
                    f = open(entry.path)
                    parse(f.read())
                    f.close()
    pass

# Parses a CSS file
def parse(s):
    global colorDictionary
    # print("Parsing File contents", s)
    cssparse.parse(s, colorDictionary)
    # Flags
    
    pass

# Generates a report
def genReport():
    global OUTPUT
    global colorDictionary

    f = open(OUTPUT, "w")
    f.write(json.dumps(colorDictionary))
    f.close()

    pass

if __name__ == "__main__":
    main()