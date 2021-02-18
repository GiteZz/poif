from abc import ABC
from enum import Enum
from pathlib import Path
from typing import List

from jinja2 import Template

from poif.dataset.base import MultiDataset
from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import DataSetObject
from poif.file_system.directory import Directory
from poif.tagged_data.base import StringBinaryData
from poif.templates import get_datasets_template_dir


class DetectionFileOutputFormat(str, Enum):
    coco = "coco"
    yolo = "yolo"
    yolov2 = "yolov2"
    yolov5 = "yolov5"


yolo_family = [
    DetectionFileOutputFormat.yolo,
    DetectionFileOutputFormat.yolov2,
    DetectionFileOutputFormat.yolov5,
]


def detection_input_to_yolo_annotation(ds_object: DataSetObject):
    output_str = ""
    yet_insert_newline = False
    for annotation in ds_object.annotations:
        if isinstance(annotation, BoundingBox):
            if yet_insert_newline:
                output_str += "\n"
            output_str += annotation.yolo_label()
            yet_insert_newline = True

    return output_str


class DetectionDataset(MultiDataset, ABC):
    def __init__(self):
        super().__init__()

        self.category_mapping = {}

    def get_classes_sorted_by_id(self) -> List[str]:
        ids = list(self.category_mapping.keys())
        assert max(ids) == len(ids) - 1

        sorted_ids = [""] * len(ids)

        for category_id, category_name in self.category_mapping.items():
            sorted_ids[category_id] = category_name

        return sorted_ids

    def create_sub_dataset_from_objects(self, new_objects: List):
        sub_dataset = DetectionDataset()
        sub_dataset.objects = new_objects
        sub_dataset.category_mapping = self.category_mapping

        return sub_dataset

    def create_file_system(self, data_format: str, base_folder: Path):
        dataset_dir = Directory()

        if data_format == DetectionFileOutputFormat.yolov5:
            data_folder = {"train": base_folder / "images" / "train", "val": base_folder / "images" / "val"}

            label_folder = {"train": base_folder / "labels" / "train", "val": base_folder / "labels" / "val"}

            sorted_ids = self.get_classes_sorted_by_id()
            needed_information = {
                "number_of_classes": len(sorted_ids),
                "classes": sorted_ids,
                "train_folder": str(data_folder["train"]),
                "val_folder": str(data_folder["val"]),
            }

            yolov5_template = get_datasets_template_dir() / "detection" / "yolov5.yaml.jinja2"

            template = Template(open(yolov5_template).read())
            rendered_template = template.render(data=needed_information)

            dataset_dir.add_data("meta.yaml", StringBinaryData(rendered_template))

            for subset in ["train", "val"]:
                for object_index, ds_object in enumerate(self.splits[subset].objects):
                    original_extension = ds_object.relative_path.split("/")[-1].split(".")[-1]
                    file_name = str(data_folder[subset] / f"{object_index}.{original_extension}")

                    dataset_dir.add_data(file_name, StringBinaryData(rendered_template))

                    label = detection_input_to_yolo_annotation(ds_object)
                    label_name = str(label_folder[subset] / f"{object_index}.txt")
                    dataset_dir.add_data(label_name, StringBinaryData(label))

        dataset_dir.setup_as_filesystem(base_folder, daemon=True)
