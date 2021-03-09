from typing import List

from poif.cache.base import CacheManager
from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.transform.base import Transformation


class AddCache(Transformation):
    """
    Adds a CacheManager to each DataSetObject in the Dataset.
    """

    def __init__(self, cache_manager: CacheManager):
        super().__init__()
        self.cache_manager = cache_manager

    def transform_single_object(self, dataset_object: DataSetObject) -> List[DataSetObject]:
        dataset_object.add_cache_manager(self.cache_manager)

        return [dataset_object]
