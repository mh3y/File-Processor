import os
import json
import argparse
from tools import Github


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


def change_to_txt(sql_files_json):
    for file in sql_files_json:
        file_path = file['fullpath']
        # if file_path.endswith(".sql"):
        new_file_path = file_path.replace('.sql', '.txt')
        os.rename(file_path, new_file_path)


# def change_to_sql(dirName):
#     for root, dirs, files in os.walk(dirName):
#         for file in files:
#             if file.endswith(".txt"):
#                 oldName = os.path.join(root, file)
#                 os.rename(oldName, oldName.replace('.txt', '.sql'))


def create_github_issue_for_blacklist(sql_files_json, header, user_name, repo_name):
    for files in sql_files_json:
        issue = {
            'owner': user_name,
            'repo': repo_name,
            'title': files["filename"],
            'body': "smells like patchouli",
            'assignees': [],
            'milestone': None,
            'labels': []
        }

        creating_issue = Github(header, user_name)
        creating_issue.create_github_issue(issue)

        # create_github_issue(header, user_name, issue)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--rename", action='store_true')
    parser.add_argument("--print", action='store_true')
    parser.add_argument("--gituser", required=False)
    parser.add_argument("--postissue", action='store_true', required=False)
    parser.add_argument("--testpostissue", action='store_true', required=False)
    parser.add_argument('--listissues', action='store_true', required=False)
    parser.add_argument("--isissueexists", type=bool, required=False)
    parser.add_argument("--dirName", type=str, required=True)
    parser.add_argument('--githubtoken')
    args = parser.parse_args()

    h = {'Accept': 'application/vnd.github+json', 'Authorization': 'token {}'.format(args.githubtoken)}

    github_repo_name = 'File-Processor'
    test_issue = {
        'owner': args.gituser,
        'repo': github_repo_name,
        'title': "bougie-02",
        'body': "smells like patchouli",
        'assignees': [],
        'milestone': None,
        'labels': []
    }

    sql_files_json = blacklist_processor(args.dirName)

    github = Github(header=h, user_name=args.gituser)
    if args.print:
        pretty_print(sql_files_json)
    if args.rename:
        change_to_txt(sql_files_json)
        pretty_print(sql_files_json)
    if args.gituser:
        github.get_github_user()
    # if args.postissue is True:
    #     create_github_issue(h, args.gituser, test_issue)
    if args.testpostissue is True:
        github.create_github_issue(test_issue)
    if args.listissues is True:
        github.list_github_issues(repo_name=github_repo_name)
    if args.isissueexists is True:
        print(args.isissueexists)

    create_github_issue_for_blacklist(sql_files_json, h, args.gituser, github_repo_name)


if __name__ == '__main__':
    main()
