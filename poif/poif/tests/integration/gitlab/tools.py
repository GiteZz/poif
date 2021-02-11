from enum import Enum
from pathlib import Path

import requests

from poif.tests.integration.gitlab.config import GitlabConfig

git_credential_file = Path.home() / ".git-credentials"


def create_repo(config: GitlabConfig, name) -> str:
    create_repo_git_api = git_api_url_from_config(config) + "projects"
    git_api_headers = headers_from_config(config)
    create_repo_param = {"name": name, "path": f"datasets-{name}"}

    create_repo_response = requests.post(create_repo_git_api, params=create_repo_param, headers=git_api_headers)
    check_if_ok(create_repo_response)
    create_repo_response.json()["http_url_to_repo"]

    return config.url + "/root/" + create_repo_param["path"] + ".git"


def check_if_ok(request):
    if not request.ok:
        print(request.content)
        raise Exception("Request not OK")


class RequestType(str, Enum):
    GET = "get"
    DELETE = "delete"
    POST = "post"


def execute_gitlab_api_call(
    api_route: str,
    config: GitlabConfig,
    params=None,
    method: RequestType = RequestType.GET,
):
    api_url = git_api_url_from_config(config) + api_route

    methods = {
        RequestType.GET: requests.get,
        RequestType.POST: requests.post,
        RequestType.DELETE: requests.delete,
    }
    method = methods[method]

    r = method(api_url, headers=headers_from_config(config), params=params)

    return r.json()


def delete_all_projects(config: GitlabConfig):
    all_projects = execute_gitlab_api_call("projects", config)

    for project in all_projects:
        project_id = project["id"]
        execute_gitlab_api_call(f"projects/{project_id}", config, method=RequestType.DELETE)


def get_existing_credentials():
    existing_credentials = []

    with open(git_credential_file, "r") as f:
        for line in f.readlines():
            url = line.split("@")[1]

            existing_credentials.append(url)

    return existing_credentials


def add_git_credential(username, password, url):
    url_without_http = url.split("/")[-1]
    url_http_part = url.split(":")[0]

    new_line = f"{url_http_part}://{username}:{password}@{url_without_http}"

    with open(git_credential_file, "a") as f:
        f.write(new_line)


def headers_from_config(config: GitlabConfig):
    return {"PRIVATE-TOKEN": config.api_key}


def git_api_url_from_config(config: GitlabConfig) -> str:
    git_url = config.url
    return f'{git_url}{"/" if git_url[-1] != "/" else ""}api/v4/'
