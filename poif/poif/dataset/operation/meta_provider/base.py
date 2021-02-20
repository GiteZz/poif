from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from poif.dataset.object.base import DataSetObject

MetaName = str


class MetaProvider(ABC):
    @abstractmethod
    def provide_meta(self, objects: List[DataSetObject]) -> List[Tuple[MetaName, Any]]:
        pass
