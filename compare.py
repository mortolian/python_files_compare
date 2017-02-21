#! /usr/bin/env python
# This is a file compare tool for command shell, created in Python. The tool was
# created to report missing or badly broken files.
#
# Maintainer    : Mortolio <hello@mortolio.com>
# Version       : 1.0
#

import hashlib
import hmac
import os
import stat
import sys
import re
import string
import logging
from time import sleep

#
# Define script colours
#
class bcolors:
    HEADER      = '\033[95m'
    OKBLUE      = '\033[94m'
    OKGREEN     = '\033[92m'
    WARNING     = '\033[93m'
    FAIL        = '\033[91m'
    ENDC        = '\033[0m'
    BOLD        = '\033[1m'
    UNDERLINE   = '\033[4m'

#
# Print help to the CLI
#
def print_help():
    print bcolors.OKGREEN
    print '''
        PYTHON FILES COMPARE TOOL
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        USAGE: compare.py {SRC} {DEST} [arguments[]]
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        ARGUMENTS:
            --help          Displays this help text
            --quick         This will skip the HASH compare of the file contents
                            which is much quicker on slower computers
            --verbose       This will print all the results to the screen and
                            not just errors
    '''
    print bcolors.ENDC
    exit(0)

#
# Return the hash of the contents of the specified file, as a hex string
#
def file_hash(name):
    f = open(name)
    h = hashlib.sha256()
    while True:
        buf = f.read(16384)
        if len(buf) == 0: break
        h.update(buf)
    f.close()
    return h.hexdigest()

#
# Traverse the specified path and update the hash with a description of its
# name and contents
#
def traverse(h, path):
    global countfiles
    global countfolders
    global passed

    rs = os.lstat(path)
    quoted_name = repr(path)

    logstring = ''
    errorfound = False

    try:
        if "desktop.ini" in path or ".DS_Store" in path or "Thumbs.db" in path:
            passed += 1
            pass
        elif stat.S_ISDIR(rs.st_mode):
            # check if the destination has this dir
            countfolders += 1
            for entry in sorted(os.listdir(path)):
                traverse(h, os.path.join(path, entry))
        elif stat.S_ISREG(rs.st_mode):
            countfiles += 1

            # Generate the destination path
            dest_path = string.replace(path, src, dest)

            logstring += "===============================================================" + "\n"
            logstring += " SRC Path: " + path + "\n"
            logstring += " DEST Path: " + dest_path + "\n"
            logstring += "---" + "\n"

            # check if the destination has this file
            if os.path.isfile(dest_path):
                logstring += " EXISTS" + "\n"
                dest_rs = os.lstat(dest_path)

                # compare the file sizes
                if dest_rs.st_size != rs.st_size:
                    logstring += "FILE SIZE MISMATCH" + "\n"
                    errorfound = True

                # compare the file content hash
                if quick == False:
                    if file_hash(path) != file_hash(dest_path):
                        logstring += " FILE CONTENT MISMATCH " + file_hash(path) + "\n"
                        errorfound = True

            else:
                # Print to screen to see progress | no verbosity check here.
                logstring += "FILE NOT FOUND: " + dest_path + "\n"
                print "FILE NOT FOUND: " + dest_path
                errorfound = True

            # Log the error to the error log file
            if errorfound == True:
                # Write to a log/report file
                with open(errorfile, "a+") as f:
                    f.write(logstring)

        else:
            passed += 1
            pass # silently skip symlinks and other special files

        # write verbose information
        if verbose == True:
            print logstring

    except Exception, e:
        # Write files which caused errors to log file
        with open(errorfile, "a+") as f:
            f.write("ERROR: " + str(e) + "\n")
        print "ERROR: " + str(e) + "\n"

#
# Main Program
#
try:
    # Check if no arguments were given
    if len(sys.argv) == 1:
        print_help()


    # Get source and destination paths
    src             = ''
    dest            = ''
    verbose         = False
    quick           = False
    errorfile       = 'error.log'
    countfiles      = 0
    countfolders    = 0
    passed          = 0

    # Process the various arguments from the CLI
    for argument in sys.argv:
        if "--help" == argument:
            print_help()
        if "--verbose" == argument:
            verbose = True
        if "--quick" == argument:
            quick = True

    if len(sys.argv) >= 3 and not "--" in sys.argv[1] and not "--" in sys.argv[2]:
        # Set the source and destination paths to compare with the relevant arguments supplied
        src             = sys.argv[1]
        dest            = sys.argv[2]

        # Start traversing over the files and directories in the src path
        print "START COMPARING FILES"

        # IF the error file exists, clear it
        if os.path.isfile(errorfile):
            os.remove(errorfile)

        h = hashlib.sha256()
        traverse(h, src)
        print "FILES: " + str(countfiles)
        print "FOLDERS: " + str(countfolders)
        print "PASSED: " + str(passed)

    else:
        print_help()

except Exception, e:
    print "ERROR: " + str(e) + "\n"
    exit(0)
