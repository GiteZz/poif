from typing import Any

from dataclasses import dataclass, field

from poif.data.cache.disk import CacheConfig
from poif.data.datapoint.base import DataPoint


@dataclass
class DiskCachedDataPoint(DataPoint):
    cache_config: CacheConfig
    _size: int = field(init=False)

    def get_cache_location(self):
        dataset_folder = self.cache_config.data_folder / self.origin.dataset_tag
        dataset_folder.mkdir(exist_ok=True)
        return dataset_folder / self.tag

    def is_in_cache(self):
        return self.get_cache_location().is_file()

    def read_from_cache(self):
        with open(self.get_cache_location(), 'rb') as f:
            file_bytes = f.read()
        return file_bytes

    def get_and_save_in_cache(self):
        file_bytes = self.origin.get_file(self.tag)
        with open(self.get_cache_location(), 'wb') as f:
            f.write(file_bytes)
        return file_bytes

    def get(self) -> Any:
        if self.is_in_cache():
            file_bytes = self.read_from_cache()
        else:
            file_bytes = self.get_and_save_in_cache()

        return self.parse_file(file_bytes, self.extension)

    def get_size(self) -> int:
        if self._size is None:
            self._size = self.origin.get_file_size(self.tag)
        return self._size