from poif.cache.base import CacheManager
from poif.dataset.object.base import DataSetObject
from poif.dataset.operation import Transformation
from typing import List


class AddCache(Transformation):
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager

    def transform_single_object(self, dataset_object: DataSetObject) -> List[DataSetObject]:
        dataset_object.add_cache_manager(self.cache_manager)

        return [dataset_object]
