from typing import Any, List, Tuple

from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.meta_provider.base import MetaName, MetaProvider


class LabelToIndex(MetaProvider):
    def provide_meta(self, objects: List[DataSetObject]) -> List[Tuple[MetaName, Any]]:
        current_index = 0
        label_to_index = {}
        for ds_object in objects:
            object_label = ds_object.label

            if object_label not in label_to_index:
                label_to_index[object_label] = current_index
                current_index += 1

            ds_object.label = label_to_index[object_label]

        index_to_label = {index: label for label, index in label_to_index.items()}
        return [("label_to_index", label_to_index), ("index_to_label", index_to_label)]
