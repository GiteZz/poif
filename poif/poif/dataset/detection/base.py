from abc import ABC
from enum import Enum
from pathlib import Path
from typing import List

from jinja2 import Template

from poif.dataset.base import MultiDataset
from poif.file_system.directory import Directory
from poif.input.annotations import BoundingBox
from poif.input.detection import DetectionInput
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


def detection_input_to_yolo_annotation(object: DetectionInput):
    output_str = ""
    yet_insert_newline = False
    for annotation in object.annotations:
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
        sub_dataset.inputs = new_objects
        sub_dataset.category_mapping = self.category_mapping

        return sub_dataset

    def create_file_system(
        self, data_format: DetectionFileOutputFormat, base_folder: Path
    ):
        dataset_dir = Directory()

        if data_format == DetectionFileOutputFormat.yolov5:
            train_data_folder = base_folder / "images" / "train"
            val_data_folder = base_folder / "images" / "val"

            train_label_folder = base_folder / "labels" / "train"
            val_label_folder = base_folder / "labels" / "val"

            sorted_ids = self.get_classes_sorted_by_id()
            needed_information = {
                "number_of_classes": len(sorted_ids),
                "classes": sorted_ids,
                "train_folder": str(train_data_folder),
                "val_folder": str(val_data_folder),
            }

            yolov5_template = (
                get_datasets_template_dir() / "detection" / "yolov5.yaml.jinja2"
            )

            template = Template(open(yolov5_template).read())
            rendered_template = template.render(data=needed_information)

            dataset_dir.add_data("meta.yaml", StringBinaryData(rendered_template))

            # TODO fix this duplication
            for object_index, ds_object in enumerate(self.val):
                # TODO fix this hacky stuff, extension needs to be known but this is not clean
                original_extension = ds_object.data.relative_path.split("/")[-1].split(
                    "."
                )[-1]
                file_name = str(
                    val_data_folder / f"{object_index}.{original_extension}"
                )

                dataset_dir.add_data(file_name, StringBinaryData(rendered_template))

                label = detection_input_to_yolo_annotation(ds_object)
                label_name = str(val_label_folder / f"{object_index}.txt")
                dataset_dir.add_data(label_name, StringBinaryData(label))

            for object_index, ds_object in enumerate(self.train):
                # TODO fix this hacky stuff, extension needs to be known but this is not clean
                original_extension = ds_object.data.relative_path.split("/")[-1].split(
                    "."
                )[-1]
                file_name = str(
                    train_data_folder / f"{object_index}.{original_extension}"
                )

                dataset_dir.add_data(file_name, StringBinaryData(rendered_template))

                label = detection_input_to_yolo_annotation(ds_object)
                label_name = str(train_label_folder / f"{object_index}.txt")
                dataset_dir.add_data(label_name, StringBinaryData(label))

        dataset_dir.setup_as_filesystem(base_folder, daemon=True)
