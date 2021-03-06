from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

import docker

from poif.tests.integration.gitlab.wait import is_alive, wait_on_url


@dataclass
class DockerConfig:
    image: str
    name: str
    restart_if_active: bool
    readiness_url: str
    commands: List[str] = field(default_factory=list)
    command: Optional[str] = None
    envs: Optional[Dict[str, str]] = None
    ports: Optional[Union[Dict[str, int], Dict[str, int]]] = None
    volumes: Optional[Dict[str, Dict[str, str]]] = None


def docker_run(config: DockerConfig):
    if not is_alive(config.readiness_url):
        client = docker.from_env()
        client.containers.prune()  # TODO dangerous

        client.containers.run(
            image=config.image,
            environment=config.envs,
            ports=config.ports,
            name=config.name,
            detach=True,
            command=config.command,
            volumes=config.volumes,
        )

        wait_on_url(config.readiness_url)
        container = client.containers.get(config.name)
        for command in config.commands:
            container.exec_run(command)
