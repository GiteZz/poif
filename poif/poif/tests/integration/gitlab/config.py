from dataclasses import dataclass, field

from poif.tests.integration.docker import DockerConfig


@dataclass
class GitlabConfig:
    port = 360
    user = 'root'
    password = 'password'
    api_key = 'root-api-key'

    url: str = field(init=False)

    def __post_init__(self):
        self.url = f'http://localhost:{self.port}'

    def get_docker_config(self) -> DockerConfig:
        image: str = 'gitlab/gitlab-ce'
        name: str = 'gitlab'

        restart_if_active: bool = True

        readiness_url = f'http://localhost:{self.port}/readiness'
        envs = {
            'GITLAB_OMNIBUS_CONFIG': f'gitlab_rails["initial_root_password"] = "{self.password}"'
        }
        ports = {
            '80': self.port
        }
        commands = [
            f'gitlab-rails runner "token = User.find_by_username(\'root\').personal_access_tokens.create(scopes: [:api], name: \'Automation token\');token.set_token(\'{self.api_key}\');token.save!"'
        ]
        docker_config = DockerConfig(image=image,
                                     name=name,
                                     restart_if_active=restart_if_active,
                                     readiness_url=readiness_url,
                                     envs=envs,
                                     ports=ports,
                                     commands=commands
                                     )

        return docker_config

