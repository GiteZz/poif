from typing import List

from poif.dataset.meta import MetaCollection
from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.meta_provider.base import MetaProvider
from poif.typing import RelFilePath


class CocoMetaProvider(MetaProvider):
    def __init__(self, annotation_file: RelFilePath):
        super().__init__()
        self.annotation_file = annotation_file

    def provide_meta(self, objects: List[DataSetObject], old_meta: MetaCollection) -> MetaCollection:
        annotation_file = None
        for ds_object in objects:
            if ds_object.relative_path == self.annotation_file:
                annotation_file = ds_object

        if annotation_file is None:
            raise Exception("Annotation file not found in objects")

        annotation_data = annotation_file.get_parsed()

        category_mapping = {}
        for category in annotation_data["categories"]:
            category_mapping[category["id"]] = category["name"]

        old_meta.index_to_label = category_mapping
        return old_meta
