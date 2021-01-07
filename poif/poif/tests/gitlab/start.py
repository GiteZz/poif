import requests
from requests import ConnectionError
import time
import docker
from docker.errors import NotFound

from poif.tests.gitlab.wait import is_alive, wait_on_url


class GitlabConfig:
    port = 360
    url = 'http://localhost:360'
    root_password = 'password'
    root_api_key = 'root-api-key'


class GitlabDockerConfig:
    image = 'gitlab/gitlab-ce'
    name = 'gitlab'
    envs = {
        'GITLAB_OMNIBUS_CONFIG': f'gitlab_rails["initial_root_password"] = "{GitlabConfig.root_password}"'
    }
    ports = {
        '80': GitlabConfig.port
    }
    restart_if_active = True
    commands = [
        'gitlab-rails runner "token = User.find_by_username(\'root\').personal_access_tokens.create(scopes: [:api], name: \'Automation token\');token.set_token(\'root-api-key\');token.save!"'
    ]


if __name__ == '__main__':
    git_url = f'http://localhost:{GitlabConfig.port}/readiness'

    if not is_alive(git_url):
        client = docker.from_env()

        client.containers.run(image=GitlabDockerConfig.image,
                              environment=GitlabDockerConfig.envs,
                              ports=GitlabDockerConfig.ports,
                              name=GitlabDockerConfig.name,
                              detach=True
                              )

        wait_on_url(git_url)
        container = client.containers.get(GitlabDockerConfig.name)
        for command in GitlabDockerConfig.commands:
            container.exec_run(command)
    else:
        print('Git was already alive')




    print('Gitlab is ready')