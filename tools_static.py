import json
import requests


class Github:

    def __init__(self, header, user_name):
        self.header = header
        self.user_name = user_name

    @staticmethod
    def get_github_user(header, user_name):
        url = 'https://api.github.com'
        url_users = '/users/'
        r = requests.get(url + url_users + user_name, headers=header)
        if r.status_code == 404:
            print(
                'Sadly the user {} does not exist, but may be a thousand years from now, he will be.'.
                format(user_name))

    @staticmethod
    def get_github_issues(user_name, header, repo_name):
        url = 'https://api.github.com'
        url_repos = '/repos/{}/{}/issues'.format(user_name, repo_name)
        r = requests.get(url + url_repos, header)
        if r.status_code != 200:
            raise Exception('Failed to get list of github issues, status_code:{}'.format(r.status_code))
        return r.json()

    @staticmethod
    def list_github_issues(user_name, header, repo_name):
        issues = Github.get_github_issues(user_name, header, repo_name)
        for issue in issues:
            print('{}, {}, {}, {}'.format(issue['id'], issue['title'], issue['state'], issue['created_at']))

    @staticmethod
    def is_github_issue_title_exists(user_name, header, repo_name, issue_title):
        issues = Github.get_github_issues(user_name, header, repo_name)
        filtered_issues = [issue for issue in issues if issue['title'] == issue_title]
        count_of_found_issues = len(filtered_issues)
        if count_of_found_issues > 0:
            return True
        else:
            return False

    @staticmethod
    def create_github_issue(user_name, header, new_issue):
        url = 'https://api.github.com'
        repo_name = 'File-Processor'
        url_repos = '/repos/{}/{}/issues'.format(user_name, header, repo_name)
        if Github.is_github_issue_title_exists(user_name, header, new_issue['repo'], new_issue['title']):
            return
        else:
            r = requests.post(url + url_repos, headers=header, data=json.dumps(new_issue))
        if r.status_code != 201:
            print('error - status code is {}'.format(r.status_code))
