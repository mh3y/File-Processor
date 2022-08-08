import os
import json
import pathlib


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def getlistofsqlfiles(dirName):
    sql_container = []
    for root, dirs, files in os.walk(r"//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts"):
        for file in files:
            if file.endswith(".sql"):
                sql_container.append(os.path.join(root, file))
    return sql_container


# def getlistofsqlfiles(dirName):
#    sql_container = []
#    for root, dirs, files in os.walk(r"//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts"):
#        for file in files:
#            if file.endswith(".sql"):
#                sql_container.append(os.path.join(root, file))
#    return sql_container

# for file in os.listdir("//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts"):
# if file.endswith(".sql"):
# print(os.path.join("//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts", file))


def main():
    dirName = '//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts'
    listOfFiles = getListOfFiles(dirName)

    keywords_file = open("keywords.json")
    keywords_json = json.load(keywords_file)
    keywords_file.close()

    for text in getlistofsqlfiles(dirName='//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts'):
        for words in keywords_json:
            if text == '//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts/.DS_Store':
                continue
            with open(text) as file:
                contents = file.read()
                search_word = words["Keyword"]
                if search_word in contents:
                    sql_specific = os.path.split(text)[1]
                    print(sql_specific)


if __name__ == '__main__':
    main()
