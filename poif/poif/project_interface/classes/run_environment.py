from dataclasses import dataclass, field
from typing import List, Union

from poif.project_interface.classes.docker_environment import DockerEnvironment

RUN_ENV_DOCKER = 0
RUN_ENV_KUBERNETES = 1


@dataclass
class RunEnvironment:
    environment: Union[DockerEnvironment]
    kube_profile: str
    # These are injected into every container
    aws_profiles: List[str] = field(default_factory=[])
    # These too
    git_profiles: List[str] = field(default_factory=[])