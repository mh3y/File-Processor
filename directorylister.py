# import os

# FILENAMES = []

# for root, dirs, files in os.walk(r".", topdown=False):

#  for filename in files:
#     if (filename.endswith(".sql")):
#          FILENAMES.append(filename)
#          print(filename)

import os

'''
    For the given path, get the List of all files in the directory tree 
'''


def getListOfFiles(dirName):
    # create a list of file and subdirectories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def main():
    dirName = '//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts'

    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)

    # Print the files
    for elem in listOfFiles:
        print(elem)

    # Get the list of all files in directory tree at given path
    listOfrandomFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfrandomFiles += [os.path.join(dirpath, file) for file in filenames]


if __name__ == '__main__':
    main()
