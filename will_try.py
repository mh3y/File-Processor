import os
import json

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
        pass
    #    print(elem)

    # Get the list of all files in directory tree at given path
    # listOfrandomFiles = list()
    # for (dirpath, dirnames, filenames) in os.walk(dirName):
    #    listOfrandomFiles += [os.path.join(dirpath, file) for file in filenames]


if __name__ == '__main__':
    main()

keywords_file = open("keywords.json")

keywords_json = json.load(keywords_file)

keywords_file.close()

# comparer = []
for words in keywords_json:
    for text in getListOfFiles(dirName='//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts'):
        if text == "//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts/.DS_Store":
            continue
        with open(text) as file:
            contents = file.read()
            search_word = words["Keyword"]
            if search_word in contents:
                print('{}: {} word found'.format(text, words["Keyword"]))
            else:
                print('{}: {} word not found'.format(text, words["Keyword"]))
print(getListOfFiles(dirName='//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts'))