from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


class FileRemote(ABC):
    """
    This is meant for remotes where data is stored as files (e.g. object stores)
    """

    @abstractmethod
    def download(self, remote_source: str) -> bytes:
        pass

    @abstractmethod
    def get_object_size(self, file_name: str):
        pass

    @abstractmethod
    def upload(self, source: bytes, remote_dest: str):
        pass

    def file_upload(self, file: Path, remote_dest: str):
        with open(file, "rb") as f:
            file_bytes = f.read()
        self.upload(file_bytes, remote_dest)

    def file_download(self, destination_file: Path, remote_source: str):
        file_bytes = self.download(remote_source)
        with open(destination_file, "wb") as f:
            f.write(file_bytes)


class HttpRemote(ABC):
    @abstractmethod
    def download(self, remote_url: str, params: dict):
        pass

    @abstractmethod
    def get_object_size(self, remote_url: str, params: dict):
        pass
