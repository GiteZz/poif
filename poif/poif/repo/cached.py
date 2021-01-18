from pathlib import Path

from poif.config.cache import CacheConfig
from poif.tagged_data.base import TaggedData
from poif.repo.base import TaggedRepo


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