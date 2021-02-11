from dataclasses import dataclass

from poif.tests.integration.docker import DockerConfig


class MinioConfig:
    port = 9000
    access_key = "minio"
    secret_key = "minio123"
    profile = "datasets"
    data_bucket = "datasets"
    readme_bucket = "readme-images"
    mount_dir = "/mnt/datasets_minio"

    def get_docker_config(self) -> DockerConfig:
        image: str = "minio/minio"
        name: str = "minio"

        restart_if_active: bool = True
        command: str = "server /data"
        envs = {
            "MINIO_ACCESS_KEY": self.access_key,
            "MINIO_SECRET_KEY": self.secret_key,
        }
        ports = {"9000": self.port}
        readiness_url = f"http://localhost:{self.port}"

        volumes = {self.mount_dir: {"bind": "/data", "mode": "rw"}}

        return DockerConfig(
            image=image,
            name=name,
            restart_if_active=restart_if_active,
            readiness_url=readiness_url,
            envs=envs,
            ports=ports,
            command=command,
            volumes=volumes,
        )
