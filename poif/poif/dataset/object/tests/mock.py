from typing import Any

from poif.dataset.object.base import DataSetObject


class TripleDataSetObject(DataSetObject):
    def output(self) -> Any:
        return self.tagged_data.get_parsed() * 3
