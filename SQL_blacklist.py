import os
import json


def getlistofsqlfiles(dirName):
    sql_container = []
    for root, dirs, files in os.walk(dirName): #TODO: tell michael about this (don't hard code the path when the path is passed in as parameter)
        for file in files:
            if file.endswith(".sql"):
                sql_container.append(os.path.join(root, file))
    return sql_container


def main():
    dirName = r'//Users//mh3y//Documents//vscode//SQL_Processor//SQL_Scripts'

    keywords_file = open("keywords.json")  # opening the JSON
    keywords_json = json.load(keywords_file)  # converting JSON file into an object
    keywords_file.close()  # closing the file

    sql_files_json = []  # creating a list
    i = 0
    for file_path in getlistofsqlfiles(dirName):
        print('**doing this file: {}'.format(file_path))
        sql_filename = os.path.split(file_path)[1]
        sql_parent_path = os.path.split(os.path.split(file_path)[0])[1]
        with open(file_path) as file:
            contents = file.read()

        list_of_words_found_for_this_file = []  # creating a list
        for words in keywords_json:  # for loop to iterate through keywords_json for "words"

            def get_whitelist_parent_path(keyword):
                if "whitelist_parent_path" in keyword:
                    return keyword["whitelist_parent_path"]
                else:
                    return None

            def is_keyword_in_file(keyword, file_content):
                return keyword in file_content

            def is_whitelisted(keyword_dict, parent_path, keyword):
                whitelist_parent_path = get_whitelist_parent_path(keyword_dict)
                if parent_path == whitelist_parent_path and keyword == keyword_dict["Keyword"]:
                    return True  # in other words, it is TRUE that the parent path is whitelisted
                else:
                    return False

            search_word = words["Keyword"]
            keyword_found = is_keyword_in_file(search_word, contents)
            qualifies_for_white_listing = is_whitelisted(words, sql_parent_path, search_word)
            # if keyword_found:
            #     print('** this file {} contains keyword {}'.format(sql_filename, search_word))
            # if qualifies_for_white_listing:
            #     print('** this file {} can be whitelisted if it contains keyword {}, as it is in parent_path {}'.format(sql_filename, search_word, sql_parent_path))

            if keyword_found and not qualifies_for_white_listing:
                # print('** this file {} is blacklisted for containing keyword {}'.format(
                #     sql_filename, search_word))
                list_of_words_found_for_this_file.append(search_word)

        if (len(list_of_words_found_for_this_file)) > 0:
            sql_files_json.append({'filename': sql_filename, 'parent_path': sql_parent_path,
                                   'fullpath': file_path, 'keyword': list_of_words_found_for_this_file})

        i = i + 1
        if i == 200:
            break

    print('total forbidden files: {}'.format(len(sql_files_json)))
    print(sql_files_json)


if __name__ == '__main__':
    main()