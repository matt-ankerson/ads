import os
'''
Given a valid path, we need a generator that yields a tuple: (dirpath, dirnames, filenames)
for each subdirectory of the directory indicated by the given path.
dirpath:    full path to the sub-directory
dirnames:   list of the names of the subdirectories within dirpath
filenames:  list of the names of the files (non-directories) within dirpath
'''


def list_contents(path):
    dirs = []
    files = []
    for child in os.listdir(path):              # for each child
        child_path = os.path.join(path, child)  # compose path to child
        if os.path.isdir(child_path):           # if the child is a directory
            dirs.append(child)
        else:       # else the child is a file
            files.append(child)
    return dirs, files                      # return the directories and files seperately

def walk_gen(path):
    dirs, files = list_contents(path)           # get contents of this path.
    yield(path, dirs, files)
    for d in dirs:                              # for each directory in this path.
        child_path = os.path.join(path, d)      # compose path to child directory.
        child_dirs, child_files = list_contents(child_path)
        for it in walk_gen(child_path):
            yield it                   # recursive call must go in loop in some form
      
for item in walk_gen('/Users/matt/Documents/Polytechnic/BITY3/repos'):
    print(item)
        