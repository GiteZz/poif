from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from poif.config import CacheConfig
from poif.data.datapoint.base import TaggedData
from poif.typing import FileHash


@dataclass
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
        with open(file, 'rb') as f:
            file_bytes = f.read()
        self.upload(file_bytes, remote_dest)

    def file_download(self, destination_file: Path, remote_source: str):
        file_bytes = self.download(remote_source)
        with open(destination_file, 'wb') as f:
            f.write(file_bytes)


class HttpRemote(ABC):
    @abstractmethod
    def download(self, remote_url: str, params: dict):
        pass

    @abstractmethod
    def get_object_size(self, remote_url: str, params: dict):
        pass


class TaggedRepo:
    @abstractmethod
    def get(self, data: TaggedData) -> bytes:
        pass

    @abstractmethod
    def get_object_size(self, data: TaggedData):
        pass

    @abstractmethod
    def upload(self, data: TaggedData):
        pass


class FileRemoteTaggedRepo(TaggedRepo):
    remote: FileRemote
    data_folder: str

    def get_remote_name(self, data: TaggedData):
        return f'{self.data_folder}/{data.tag[:2]}/{data.tag[2:]}'

    def get(self, data: TaggedData) -> bytes:
        return self.remote.download(self.get_remote_name(data))

    def get_object_size(self, data: TaggedData):
        return self.remote.get_object_size(self.get_remote_name(data))

    def upload(self, data: TaggedData):
        self.remote.upload(data.get(), self.get_remote_name(data))


class CachedTaggedRepo(TaggedRepo):
    original_repo: TaggedRepo
    cache_config: CacheConfig

    def get_cache_location(self, data: TaggedData):
        data_location = self.cache_config.data_storage_location / data.tag[:2] / data.tag[2:]
        data_location.parent.mkdir(exist_ok=True, parents=True)

        return data_location

    def write_to_cache(self, data: TaggedData):
        self.write_bytes_to_location(data.get(), self.get_cache_location(data))

    def write_bytes_to_location(self, data_bytes: bytes, location: Path):
        with open(location, 'wb') as f:
            f.write(data_bytes)

    def is_in_cache(self, data: TaggedData) -> bool:
        return self.get_cache_location(data).is_file()

    def get_from_cache(self, data: TaggedData) -> bytes:
        with open(self.get_cache_location(data), 'rb') as f:
            file_bytes = f.read()
        return file_bytes

    def get_object_size(self, data: TaggedData) -> int:
        # TODO cache in memory or not
        return self.original_repo.get_object_size(data)

    def upload(self, data: TaggedData):
        if self.cache_config.cache_uploads and not self.is_in_cache(data):
            self.write_to_cache(data)

        self.original_repo.upload(data)

    def get(self, data: TaggedData) -> bytes:
        if self.is_in_cache(data):
            return self.get_from_cache(data)

        data_bytes = data.get()
        self.write_bytes_to_location(data_bytes, self.get_cache_location(data))

        return data_bytes