# DirSearch
**A simple python program that lets you easily search for expressions in compliacted filesystems supporting various searching features, like search by distance.**

## How to use it
Download the search.py source file.

This is a standalone commandline tool, supporting basic flags.

### Windows

1. Create a **.bat** file that will call **seach.py**, system path is suggested. This **.bat** file will serve as an alias for the actual **search.py** file. In this example ```psearch.bat``` will be used.
2. Open the **psearch.bat** file and add
```
@echo off
python "<path/to/search.py>" %*
```
4. **(optional)**: If psearch.bat is not already on the system path, add it:
Environment variables > System environment variables > Add to the "Path" variable the location of the file, or move the file to a directory already present in the PATH

### Linux

1. Place **search.py** in a directory on the system PATH. Recommended: ```/usr/local/bin``` or ```~/bin```. \
Alternatively, put it anywhere and add the folder to the PATH: open ```~/.bashrc``` and add the line ```export PATH="$PATH:/path/to/directory"```, then resource the terminal.
2. Add executable permission to **search.py** by writing ```chmod +x /path/to/search.py``` in the terminal.
3. Add ```#!/usr/bin/env python3``` to the top of **search.py**. Now you can also remove the .py extension too for easier access.
