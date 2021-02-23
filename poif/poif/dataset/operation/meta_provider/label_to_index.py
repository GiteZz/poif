from typing import List

from poif.dataset.meta import MetaCollection
from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.meta_provider.base import MetaProvider


class LabelToIndex(MetaProvider):
    def provide_meta(self, objects: List[DataSetObject], old_meta: MetaCollection) -> MetaCollection:
        current_index = 0
        label_to_index = {}
        for ds_object in objects:
            object_label = ds_object.label

            if object_label not in label_to_index:
                label_to_index[object_label] = current_index
                current_index += 1

            ds_object.label = label_to_index[object_label]

        index_to_label = {index: label for label, index in label_to_index.items()}

        old_meta.index_to_label = index_to_label
        old_meta.label_to_index = label_to_index

        return old_meta
