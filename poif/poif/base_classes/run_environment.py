from dataclasses import dataclass, field
from typing import List
from poif.base_classes.docker_environment import DockerEnvironment

RUN_ENV_DOCKER = 0
RUN_ENV_KUBERNETES = 1


@dataclass
class RunEnvironment:
    docker_environment: DockerEnvironment
    environment: int  # TODO Enum?
    kube_profile: str
    # These are injected into every container
    aws_profiles: List[str] = field(default_factory=[])
    # These too
    git_profiles: List[str] = field(default_factory=[])