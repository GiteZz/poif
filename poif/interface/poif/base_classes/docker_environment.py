from dataclasses import dataclass


@dataclass
class DockerEnvironment:
    docker_file: str = None
    from_requirements: str = None
    from_conda: str = None