import os
import json
import argparse
import requests


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


def get_github_user(user_name):
    url = 'https://api.github.com'
    url_users = '/users/'
    # h = {'Accept': 'application/vnd.github+json', 'Authorization': 'token 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'}
    print('TODO: call {}{}{}'.format(url, url_users, user_name))
    r = requests.get(url + url_users + user_name, headers=h)
    print(r.json())
    print('Status Code returned:{}'.format(r.status_code))
    if r.status_code == 404:
        print('Sadly the user {} does not exist, but may be a thousand years from now, he will be.'.format(user_name))


def create_github_issue(header, user_name, new_issue):
    url = 'https://api.github.com'
    repo_name = 'File-Processor'
    url_repos = '/repos/{}/{}/issues'.format(user_name, repo_name)
    # h = {'Accept': 'application/vnd.github+json', 'Authorization': 'token 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'}

    if is_github_issue_title_exists(header, new_issue['owner'], new_issue['repo'], new_issue['title']):
        return
    else:
        r = requests.post(url + url_repos, headers=header, data=json.dumps(new_issue))
    # print(r.json())
    # print('Status Code returned:{}'.format(r.status_code))
    if r.status_code != 201:
        print('error - status code is {}'.format(r.status_code))


def get_github_issues(header, user_name, repo_name):
    url = 'https://api.github.com'
    url_repos = '/repos/{}/{}/issues'.format(user_name, repo_name)
    # h = {'Accept': 'application/vnd.github+json', 'Authorization': 'token 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'}
    r = requests.get(url + url_repos, headers=header)
    if r.status_code != 200:
        raise Exception('Failed to get list of github issues, status_code:{}'.format(r.status_code))
    return r.json()


def list_github_issues(header, user_name, repo_name):
    issues = get_github_issues(header, user_name=user_name, repo_name=repo_name)
    for issue in issues:
        print('{}, {}, {}, {}'.format(issue['id'], issue['title'], issue['state'], issue['created_at']))


def is_github_issue_title_exists(header, user_name, repo_name, issue_title):
    issues = get_github_issues(header, user_name=user_name, repo_name=repo_name)
    filtered_issues = [issue for issue in issues if issue['title'] == issue_title]
    count_of_found_issues = len(filtered_issues)
    if count_of_found_issues > 0:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rename", action='store_true')
    parser.add_argument("--print", action='store_true')
    parser.add_argument("--gituser", required=False)
    parser.add_argument("--postissue", action='store_true', required=False)
    parser.add_argument('--listissues', required=False, action='store_true')
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

    # print(args)

    if args.print:
        pretty_print(sql_files_json)
    if args.rename:
        change_to_txt(sql_files_json)
        pretty_print(sql_files_json)
    # if args.gituser:
    #     get_github_user(args.gituser)
    if args.postissue is True:
        create_github_issue(h, args.gituser, test_issue)
    if args.listissues is True:
        list_github_issues(user_name=args.gituser, repo_name=github_repo_name)
    if args.isissueexists is True:
        print(args.isissueexists)


if __name__ == '__main__':
    main()
