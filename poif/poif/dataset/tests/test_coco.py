import random
from pathlib import Path

import pytest

from poif.dataset.detection.base import DetectionFileOutputFormat
from poif.dataset.detection.coco import CocoDetectionDataset, detection_collection_to_coco_dict
from poif.input.annotations import BoundingBox
from poif.input.detection import DetectionInput
from poif.tagged_data.disk import DiskData
from poif.tagged_data.tests.mock import MockTaggedData
from poif.tests import get_img, get_temp_path


def get_random_bounding_box(img_width=1280, img_height=720, amount_of_classes=3):
    min_width = img_width // 8
    min_height = img_height // 8

    class_id = random.randint(0, amount_of_classes - 1)
    x = random.randint(0, img_width - 1 - min_width)
    y = random.randint(0, img_height - 1 - min_height)
    w = random.randint(0, img_width - x)
    h = random.randint(0, img_height - y)

    return BoundingBox(
        label=class_id,
        x=x / img_width,
        y=y / img_height,
        w=w / img_width,
        h=h / img_height,
    )


@pytest.fixture
def detection_collection(
    image_count=15,
    max_annotations_per_image=5,
    img_width=1280,
    img_height=720,
    amount_of_classes=3,
):
    images = [
        DetectionInput(
            data=MockTaggedData(f"{i}.jpg", get_img()),
            width=img_width,
            height=img_height,
        )
        for i in range(image_count)
    ]
    for image in images:
        img_annotation_iterations = random.randint(1, max_annotations_per_image - 1)
        for _ in range(img_annotation_iterations):
            image.add_bounding_box(
                get_random_bounding_box(
                    img_width=img_width,
                    img_height=img_height,
                    amount_of_classes=amount_of_classes,
                )
            )

    return images


def test_coco(detection_collection):
    coco_dict = detection_collection_to_coco_dict(detection_collection)
    annotation_file = MockTaggedData(relative_path="train.json", data=coco_dict)

    tagged_data = [annotation_file] + [detection_input.data for detection_input in detection_collection]
    ds = CocoDetectionDataset(annotation_files={"train": "train.json"}, data_folders={"train": ""})

    ds.form(tagged_data)

    # TODO check


def test_real_coco():
    disk_loc = get_temp_path()
    disk_path = Path("/home/gilles/datasets/mask/")

    tagged_data = DiskData.from_folder(disk_path)
    ds = CocoDetectionDataset(annotation_files={"main": "ann.json"}, data_folders={"main": "images"})
    ds.form(tagged_data)

    ds.random_split({"train": 0.7, "val": 0.3})

    ds.create_file_system(DetectionFileOutputFormat.yolov5, disk_loc)
