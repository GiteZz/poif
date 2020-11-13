import pathlib
import requests

git_credential_file = pathlib.Path.home() / '.git-credentials'


def get_existing_credentials():
    existing_credentials = []

    with open(git_credential_file, 'r') as f:
        for line in f.readlines():
            url = line.split('@')[1]

            existing_credentials.append(url)

    return existing_credentials


def add_git_credential(username, password, url):
    url_without_http = url.split('/')[-1]
    url_http_part = url.split(':')[0]

    new_line = f'{url_http_part}://{username}:{password}@{url_without_http}'

    with open(git_credential_file, 'a') as f:
        f.write(new_line)


def headers_from_config(config):
    return {
        'PRIVATE-TOKEN': config['git_api_key']
    }


def git_api_url_from_config(config):
    return f'{config["git_url"]}{"/" if config["git_url"][-1] != "/" else ""}/api/v4/'


def get_group_id(name, config):
    group_info_response = requests.get(
        git_api_url_from_config(config) + f'groups/{name}',
        headers=headers_from_config(config)
        )

    return group_info_response.json()['id']


def create_repo(config, share_group, name) -> str:
    create_repo_git_api = git_api_url_from_config(config) + 'projects'
    git_api_headers = headers_from_config(config)
    create_repo_param = {
        'name': name,
        'path': f'datasets-{name}'
    }

    create_repo_response = requests.post(create_repo_git_api, params=create_repo_param, headers=git_api_headers)
    if not create_repo_response.ok:
        print(create_repo_response)
    project_id = create_repo_response.json()['id']
    repo_url = create_repo_response.json()['http_url_to_repo']

    group_id = get_group_id(share_group, config)

    share_project_param = {
        'group_access': 30,
        'group_id': group_id
    }
    share_repo_git_api = git_api_url_from_config(config) + f'projects/{project_id}/share'
    requests.post(share_repo_git_api, params=share_project_param, headers=git_api_headers)

    return repo_url

