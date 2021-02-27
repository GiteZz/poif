import json
from pathlib import Path

from poif.dataset.base import MultiDataset
from poif.dataset.file_system.base import FileSystemCreator
from poif.file_system.directory import Directory
from poif.tagged_data.base import StringBinaryData
from poif.utils.coco import detection_collection_to_coco_dict


class COCOFileSystem(FileSystemCreator):
    def create(self, dataset: MultiDataset, base_dir: Path, daemon=True):
        dataset_dir = Directory()

        for subset in dataset.available_sub_datasets:
            annotation_dict = detection_collection_to_coco_dict(
                dataset.splits[subset].objects, dataset.meta.index_to_label
            )
            annotation_json = json.dumps(annotation_dict)

            dataset_dir.add_data(f"{subset}.json", StringBinaryData(annotation_json))

            for ds_object in dataset.splits[subset].objects:
                dataset_dir.add_data(ds_object.relative_path, ds_object)

        dataset_dir.setup_as_filesystem(base_dir, daemon=daemon)
