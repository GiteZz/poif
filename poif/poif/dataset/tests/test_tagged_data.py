from typing import Any, List

import pytest

from poif.dataset.tagged_data import TaggedDataDataset
from poif.input.transform.template import DropByTemplate
from poif.tagged_data.base import TaggedData
from poif.tests import get_img


class MockTaggedData(TaggedData):
    def __init__(self, relative_path: str, data: Any):
        super().__init__(relative_path)
        self.data = data

    @property
    def size(self) -> int:
        return 0

    def get(self) -> bytes:
        raise NotImplementedError

    def get_parsed(self) -> Any:
        return self.data


@pytest.fixture
def classification_dataset(imgs_per_set=10, amount_categories=5) -> List[TaggedData]:
    data_points = []
    sub_datasets = ["train", "val", "test"]
    labels = [f"cat{i}" for i in range(amount_categories)]

    for sub_dataset in sub_datasets:
        for label in labels:
            data_points.extend(
                [
                    MockTaggedData(f"{sub_dataset}/{label}/rgb_{i}.jpg", get_img())
                    for i in range(imgs_per_set)
                ]
            )
            data_points.extend(
                [
                    MockTaggedData(f"{sub_dataset}/{label}/bw_{i}.jpg", get_img())
                    for i in range(imgs_per_set)
                ]
            )

    return data_points


@pytest.fixture
def mask_dataset(imgs_per_set=10, sub_datasets=None) -> List[TaggedData]:
    if sub_datasets is None:
        sub_datasets = ["train", "val", "test"]
    data_points = []

    for sub_dataset in sub_datasets:
        data_points.extend(
            [
                MockTaggedData(f"{sub_dataset}/mask_{i}.jpg", get_img())
                for i in range(imgs_per_set)
            ]
        )
        data_points.extend(
            [
                MockTaggedData(f"{sub_dataset}/image_{i}.jpg", get_img())
                for i in range(imgs_per_set)
            ]
        )

    return data_points


def test_combining_mask_img(mask_dataset):
    operation_list = [
        CombineByTemplate({"image": "*/image*.jpg", "mask": "*/mask*.jpg"})
    ]

    ds = TaggedDataDataset(operations=operation_list)
    ds.form(mask_dataset)

    collected_images = [ds_input.image for ds_input in ds.inputs]
    collected_masks = [ds_input.mask for ds_input in ds.inputs]

    for image, mask in zip(collected_images, collected_masks):
        assert collected_images.count(image) == 1
        assert collected_masks.count(mask) == 1

    for ds_input in ds:
        img_data = ds_input.image.relative_path.replace("image", "")
        mask_data = ds_input.mask.relative_path.replace("mask", "")
        assert img_data == mask_data


def test_dropping(mask_dataset):
    operation_list = [DropByTemplate("*/mask*.jpg")]

    ds = TaggedDataDataset(operations=operation_list)
    ds.form(mask_dataset)

    assert len(ds) * 2 == len(mask_dataset)

    for ds_input in ds:
        assert "mask" not in ds_input.relative_path


def test_splitting(mask_dataset):
    operation_list = [SplitByTemplate("{{ subset }}/*")]

    ds = TaggedDataDataset(operations=operation_list)
    ds.form(mask_dataset)

    assert len(ds.train) + len(ds.test) + len(ds.val) == len(ds)
    assert len(ds) == len(mask_dataset)


def test_splitting_and_combining(mask_dataset):
    operation_list = [
        SplitByTemplate("{{ subset }}/*"),
        CombineByTemplate({"image": "*/image*.jpg", "mask": "*/mask*.jpg"}),
    ]

    ds = TaggedDataDataset(operations=operation_list)
    ds.form(mask_dataset)

    assert (len(ds.train) + len(ds.test) + len(ds.val)) * 2 == len(ds)
