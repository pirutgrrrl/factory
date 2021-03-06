#!/usr/bin/env python


# Map Converter
#
# Converts a resource output generated by the DeRez tool and focuses on 
# MapL, BakL and Asmb resource forks, outputting them as space delimited
# decimals to MAP files
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
    count = 0
    line_length = 0
    type = ""

    for line in file.readlines():
        if output and "};" in line:
            output.close()
            output = None
        elif "MapL" in line or "BakL" in line or "Asmb" in line:
            if "MapL" in line:
                type = "layout"
                line_length = 16
            elif "BakL" in line:
                type = "background"
                line_length = 16
            elif "Asmb" in line:
                type = "assembly"
                line_length = 11

            count = 0
            output = open(os.path.join(options.output_dir, "%s_%s.map" % (line[line.find("(") + 1:line.find(")")], type)), "wb")
        elif output:
            for part in line[line.find('"') + 1:line.find('"', line.find('"') + 1)].split(" "):
                for i in range(2):
                    if count == line_length:
                        output.write("\n")
                        count = 0

                    bit = part[i * 2:i * 2 + 2]

                    if len(bit) > 0:
                        output.write("%03d " % int(bit, 16))

                        count += 1

    file.close()


if __name__ == "__main__":
    main()
