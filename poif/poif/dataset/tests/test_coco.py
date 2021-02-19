import random

import pytest

from poif.dataset.base import MultiDataset
from poif.dataset.operation.transform.coco import SingleCoco
from poif.utils.coco import detection_collection_to_coco_dict
from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import DataSetObject
from poif.tagged_data.tests.mock import MockTaggedData
from poif.tests import get_img


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
    images = [DataSetObject(tagged_data=MockTaggedData(f"{i}.jpg", get_img())) for i in range(image_count)]
    for image in images:
        img_annotation_iterations = random.randint(1, max_annotations_per_image - 1)
        for _ in range(img_annotation_iterations):
            image.add_annotation(
                get_random_bounding_box(
                    img_width=img_width,
                    img_height=img_height,
                    amount_of_classes=amount_of_classes,
                )
            )
    label_mapping = {label_index: f"label_{label_index}" for label_index in range(amount_of_classes)}
    return images, label_mapping


def test_coco(detection_collection):
    images, label_mapping = detection_collection
    coco_dict = detection_collection_to_coco_dict(images, label_mapping)
    annotation_file = MockTaggedData(relative_path="train.json", data=coco_dict)

    tagged_data = [annotation_file] + [detection_input for detection_input in images]
    coco_transform = SingleCoco(annotation_file='train.json', data_folder="")

    ds = MultiDataset(operations=[coco_transform])
    ds.form(tagged_data)

    assert len(ds) == len(images)


    # TODO check


# def test_real_coco():
#     disk_loc = get_temp_path()
#     disk_path = Path("/home/gilles/datasets/mask/")
#
#     tagged_data = DiskData.from_folder(disk_path)
#     ds = CocoDetectionDataset(annotation_files={"main": "ann.json"}, data_folders={"main": "images"})
#     ds.add_transformation(RandomSplitter({"train": 0.7, "val": 0.3}))
#     ds.form(tagged_data)
#
#     ds.create_file_system(DetectionFileOutputFormat.yolov5, disk_loc)
