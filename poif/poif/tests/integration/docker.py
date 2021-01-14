from dataclasses import dataclass, field
from typing import Dict, List, Union

import docker

from poif.tests.integration.gitlab.wait import is_alive, wait_on_url


@dataclass
class DockerConfig:
    image: str
    name: str
    restart_if_active: bool
    readiness_url: str
    command: str = None
    commands: List[str] = field(default_factory=list)
    envs: Dict[str, str] = None
    ports: Dict[Union[str, int], Union[str, int]] = None
    volumes: Dict[str, Dict[str, str]] = None


def docker_run(config: DockerConfig):
    if not is_alive(config.readiness_url):
        client = docker.from_env()
        client.containers.prune() # TODO dangerous

        client.containers.run(image=config.image,
                              environment=config.envs,
                              ports=config.ports,
                              name=config.name,
                              detach=True,
                              command=config.command,
                              volumes=config.volumes
                              )

        wait_on_url(config.readiness_url)
        container = client.containers.get(config.name)
        for command in config.commands:
            container.exec_run(command)