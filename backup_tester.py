import os
import json


#  import pathlib


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

    keywords_file = open("keywords.json")  # opening the JSON
    keywords_json = json.load(keywords_file)  # converting JSON file into an object
    keywords_file.close()  # closing the file

    sql_files_json = []  # creating a list
    for file_path in getlistofsqlfiles(dirName='//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts'):
        list_of_words_found_for_this_file = []  # creating a list
        for words in keywords_json:  # for loop to iterate through keywords_json for "words"
            #  print(words)
            with open(file_path) as file:
                contents = file.read()
                search_word = words["Keyword"]
            if "whitelist" in words:
                print("whitelist exists")
            else:
                continue

                if file_path == words["whitelist"]:
                    continue
                else:
                    if search_word in contents:
                        list_of_words_found_for_this_file.append(search_word)
        if (len(list_of_words_found_for_this_file)) > 0:
            # print(file_path)
            # print(list_of_words_found_for_this_file)
            # print(len(list_of_words_found_for_this_file))
            sql_filename = os.path.split(file_path)[1]
            sql_parent_path = os.path.split(os.path.split(file_path)[0])[1]
            sql_files_json.append({'filename': sql_filename, 'parent_path': sql_parent_path,
                                   'fullpath': file_path, 'keyword': list_of_words_found_for_this_file})

        print(sql_files_json)


if __name__ == '__main__':
    main()
