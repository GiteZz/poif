from typing import Optional

from poif.dataset.meta import MetaCollection


class Operation:
    def __init__(self):
        super().__init__()
        self._dataset_meta: Optional[MetaCollection] = None

    def set_meta(self, meta: MetaCollection):
        self._dataset_meta = meta

    def get_meta(self) -> Optional[MetaCollection]:
        return self._dataset_meta
