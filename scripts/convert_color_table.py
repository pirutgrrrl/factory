#!/usr/bin/env python


# Color Table Converter
#
# Converts a resource output generated by the DeRez tool and focuses on 
# PICT forks, exporting the color table
#
# Taylan Pince (taylanpince at gmail dot com)


import os
import sys

from binascii import a2b_hex
from optparse import OptionParser


def main():
    parser = OptionParser(usage="Usage: %prog [options] --file=FILE_PATH", version="%prog 0.1")

    parser.set_defaults(output_dir=os.getcwd())
    parser.add_option("-f", "--file", dest="file_path", help="Path to the resource file to parse")
    parser.add_option("-o", "--output-dir", dest="output_dir", help="Output path, by default the current working directory")

    (options, args) = parser.parse_args()
    
    if not options.file_path:
        parser.error("You have to specify a file path")

    file = open(options.file_path, "r")
    output = None

    for line in file.readlines():
        if output and "};" in line:
            output.close()
            output = None
        elif "PICT" in line and "9877" in line:
            output = open(os.path.join(options.output_dir, "colors.act"), "wb")
        elif output:
            output.write(a2b_hex(line[line.find('"') + 1:line.find('"', line.find('"') + 1)].replace(" ", "")))  

    file.close()


if __name__ == "__main__":
    main()
