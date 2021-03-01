from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml

from poif.dataset.base import Dataset
from poif.dataset.detection.base import detection_input_to_yolo_annotation
from poif.dataset.file_system.base import FileSystemCreator
from poif.file_system.directory import Directory
from poif.tagged_data.base import StringBinaryData


@dataclass
class Yolov5MetaFile:
    train_image_folder: Path
    val_image_folder: Path
    # number of classes
    number_of_classes: int
    # class names
    class_names: List[str]

    def to_file(self) -> str:
        return yaml.dump(
            {
                "train": str(self.train_image_folder),
                "val": str(self.val_image_folder),
                "nc": self.number_of_classes,
                "names": self.class_names,
            }
        )


class Yolov5FileSystem(FileSystemCreator):
    def create(self, dataset: Dataset, base_dir: Path) -> Directory:
        dataset_dir = Directory()

        data_folder = {"train": base_dir / "images" / "train", "val": base_dir / "images" / "val"}

        label_folder = {"train": base_dir / "labels" / "train", "val": base_dir / "labels" / "val"}

        sorted_ids = self.get_classes_sorted_by_id(dataset)

        meta = Yolov5MetaFile(
            train_image_folder=data_folder["train"],
            val_image_folder=data_folder["val"],
            number_of_classes=len(sorted_ids),
            class_names=sorted_ids,
        )

        dataset_dir.add_data("meta.yaml", StringBinaryData(meta.to_file()))

        for subset in ["train", "val"]:
            for object_index, ds_object in enumerate(dataset.splits[subset].objects):
                original_extension = ds_object.relative_path.split("/")[-1].split(".")[-1]
                file_name = str(data_folder[subset] / f"{object_index}.{original_extension}")

                dataset_dir.add_data(file_name, ds_object)

                label = detection_input_to_yolo_annotation(ds_object)
                label_name = str(label_folder[subset] / f"{object_index}.txt")
                dataset_dir.add_data(label_name, StringBinaryData(label))

        return dataset_dir
