# Intro
This is a file compare tool for command shell, created in Python. The tool was
created to report missing or badly broken files into an error log file to allow
you to identify any problems.

# Use Case
If you copy files from one directory to another, you might want to use this
tool to see if all the files arrived on the other side correctly.

# How to use it
```
USAGE: compare.py {SRC} {DEST} [arguments[]]

ARGUMENTS:
--help          Displays this help text
--quick         This will skip the HASH compare of the file contents which is much quicker on slower computers
--verbose       This will print all the results to the screen and not just errors
```

After running the compare.py, you will notice a error.log file in the same directory
this is where all the errors will be contained.


# Possible Improvements
* Allow user to specify error log filename
* Verbose report on the screen can be better
* Test in Windows

# Contribute
You are welcome to fork and contribute to this project.

# Technology
* Python 2.7
* OS: Should work on any OS with Python installed (Not tested)
* GIT
