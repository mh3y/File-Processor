import os
import json
import argparse


def get_list_of_sql_files(dirName):
    sql_container = []
    for root, dirs, files in os.walk(dirName):
        for file in files:
            if file.endswith(".sql"):
                sql_container.append(os.path.join(root, file))

    return sql_container


def blacklist_processor(dirName):
    keywords_file = open("keywords.json")
    keywords_json = json.load(keywords_file)
    keywords_file.close()

    sql_files_json = []
    i = 0
    for file_path in get_list_of_sql_files(dirName):
        sql_filename = os.path.split(file_path)[1]
        sql_parent_path = os.path.split(os.path.split(file_path)[0])[1]
        with open(file_path) as file:
            contents = file.read()

        list_of_words_found_for_this_file = []
        for words in keywords_json:

            def get_whitelist_parent_path(keyword):
                if "whitelist_parent_path" in keyword:
                    return keyword["whitelist_parent_path"]
                else:
                    return []

            # def is_keyword_in_file(keyword, file_content):
            #     return keyword in file_content

            def is_whitelisted(keyword_dict, parent_path, json_dict):
                whitelist_parent_path = get_whitelist_parent_path(keyword_dict)
                if parent_path in whitelist_parent_path and json_dict == keyword_dict["Keyword"]:
                    return True
                else:
                    return False

            search_word = words["Keyword"]
            keyword_found = search_word in contents
            # keyword_found = is_keyword_in_file(search_word, contents)
            qualifies_for_white_listing = is_whitelisted(words, sql_parent_path, search_word)

            if keyword_found and not qualifies_for_white_listing:
                list_of_words_found_for_this_file.append(search_word)

        if (len(list_of_words_found_for_this_file)) > 0:
            sql_files_json.append({'filename': sql_filename, 'parent_path': sql_parent_path,
                                   'fullpath': file_path, 'keyword': list_of_words_found_for_this_file})

        i = i + 1
        if i == 200:
            break

    return sql_files_json


def pretty_print(sql_files_json):
    print('total forbidden files: {}'.format(len(sql_files_json)))
    for file in sql_files_json:
        parent_path = file["parent_path"]
        sql_filename = file["filename"]
        search_word = ' and '.join(file["keyword"])
        print("{} in {} is blacklisted for having keywords '{}'".format(sql_filename, parent_path, search_word))
    return pretty_print


# def change_to_txt(sql_files_json):
#     for sql_file in sql_files_json:
#         if sql_file["sql_filename"].endswith(".sql"):
#         # sql_filename.rename(sql_filename.with_suffix('.txt'))


# def change_to_txt(sql_container):
#     for file in sql_container:
#         # if sql_container.endswith(".sql"):
#         file.rename(file.with_suffix('.txt'))

def change_to_txt(sql_files_json):
    for file in sql_files_json:
        file_path = file['fullpath']
        # if file_path.endswith(".sql"):
        new_file_path = file_path.replace('.sql', '.txt')
        os.rename(file_path, new_file_path)

#
# def change_to_sql(dirName):
#     for root, dirs, files in os.walk(dirName):
#         for file in files:
#             if file.endswith(".txt"):
#                 oldName = os.path.join(root, file)
#                 os.rename(oldName, oldName.replace('.txt', '.sql'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dirName")
    args = parser.parse_args()

    sql_files_json = blacklist_processor(args.dirName)
    pretty_print(sql_files_json)
    change_to_txt(sql_files_json)
    # change_to_sql(args.dirName)


if __name__ == '__main__':
    main()
