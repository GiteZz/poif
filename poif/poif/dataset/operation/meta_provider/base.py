from abc import ABC, abstractmethod
from typing import List

from poif.dataset.meta import MetaCollection
from poif.dataset.object.base import DataSetObject

MetaName = str


class MetaProvider(ABC):
    @abstractmethod
    def provide_meta(self, objects: List[DataSetObject], original_meta: MetaCollection) -> MetaCollection:
        pass
