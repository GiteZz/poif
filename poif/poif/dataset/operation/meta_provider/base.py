from abc import ABC, abstractmethod
from typing import List

from poif.dataset.meta import MetaCollection
from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.base import Operation

MetaName = str


class MetaProvider(Operation, ABC):
    """
    The MetaProvider operation is used to transform the original MetaCollection as well as transforming
    objects that could be influenced by changing the meta. An example of this is changing the actual label to
    and integer. This adds the mapping to the meta as well as changes the objects.
    """

    @abstractmethod
    def provide_meta(self, objects: List[DataSetObject], original_meta: MetaCollection) -> MetaCollection:
        pass
