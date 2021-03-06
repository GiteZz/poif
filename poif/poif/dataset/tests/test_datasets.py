from typing import List

import numpy as np
import pytest

from poif.dataset.base import Dataset
from poif.dataset.object.base import DataSetObject
from poif.dataset.object.output import single_mask_output
from poif.dataset.operation.split.template import SplitByTemplate
from poif.dataset.operation.transform.template import DropByTemplate, MaskByTemplate, MaskTemplate
from poif.tagged_data.base import TaggedData
from poif.tagged_data.tests.mock import MockTaggedData
from poif.tests import get_img


def triple_output(ds_object: DataSetObject) -> int:
    parsed_output = ds_object.get_parsed()
    assert isinstance(parsed_output, int)
    return parsed_output * 3


def test_different_input():
    ds_tagged_data = [MockTaggedData(f"{i}.png", i) for i in range(10)]
    ds = Dataset(output_function=triple_output)

    ds.form(ds_tagged_data)

    possible_values = {i * 3 for i in range(10)}
    for ds_object in ds:
        assert ds_object in possible_values
        possible_values.remove(ds_object)


@pytest.fixture
def classification_dataset(imgs_per_set=10, amount_categories=5) -> List[TaggedData]:
    data_points: List[TaggedData] = []
    sub_datasets = ["train", "val", "test"]
    labels = [f"cat{i}" for i in range(amount_categories)]

    for sub_dataset in sub_datasets:
        for label in labels:
            data_points.extend(
                [MockTaggedData(f"{sub_dataset}/{label}/rgb_{i}.jpg", get_img()) for i in range(imgs_per_set)]
            )
            data_points.extend(
                [MockTaggedData(f"{sub_dataset}/{label}/bw_{i}.jpg", get_img()) for i in range(imgs_per_set)]
            )

    return data_points


@pytest.fixture
def mask_dataset(imgs_per_set=10, sub_datasets=None) -> List[TaggedData]:
    if sub_datasets is None:
        sub_datasets = ["train", "val", "test"]
    data_points: List[TaggedData] = []

    for sub_dataset in sub_datasets:
        data_points.extend([MockTaggedData(f"{sub_dataset}/mask_{i}.jpg", get_img()) for i in range(imgs_per_set)])
        data_points.extend([MockTaggedData(f"{sub_dataset}/image_{i}.jpg", get_img()) for i in range(imgs_per_set)])

    return data_points


def test_combining_mask_img(mask_dataset):
    mask_template = MaskTemplate(image="{{subset}}/image_{{img_id}}.jpg", mask="{{subset}}/mask_{{img_id}}.jpg")
    operation_list = [MaskByTemplate(mask_template)]

    ds = Dataset(operations=operation_list, output_function=single_mask_output)
    ds.form(mask_dataset)

    assert len(ds.objects) == len(mask_dataset) // 2

    for ds_object in ds.objects:
        img, mask = ds_object.output()
        assert isinstance(img, np.ndarray)
        assert isinstance(mask, np.ndarray)

        img_path = ds_object.relative_path
        mask_path = ds_object.annotations[0].relative_path

        assert "image" in img_path
        assert "mask" in mask_path

        img_data = img_path.replace("image", "")
        mask_data = mask_path.replace("mask", "")

        assert img_data == mask_data


def test_dropping(mask_dataset):
    operation_list = [DropByTemplate("*/mask*.jpg")]

    ds = Dataset(operations=operation_list)
    ds.form(mask_dataset)

    assert len(ds) * 2 == len(mask_dataset)

    for ds_object in ds.objects:
        assert "mask" not in ds_object.relative_path


def test_splitting(mask_dataset):
    operation_list = [SplitByTemplate("{{ subset }}/*")]

    ds = Dataset(operations=operation_list)
    ds.form(mask_dataset)

    assert len(ds.train) + len(ds.test) + len(ds.val) == len(ds)
    assert len(ds) == len(mask_dataset)


def test_splitting_and_combining(mask_dataset):
    mask_template = MaskTemplate(image="{{subset}}/image_{{img_id}}.jpg", mask="{{subset}}/mask_{{img_id}}.jpg")
    operation_list = [
        SplitByTemplate("{{ subset }}/*"),
        MaskByTemplate(mask_template),
    ]

    ds1 = Dataset(operations=operation_list)
    ds1.form(mask_dataset)

    assert (len(ds1.train) + len(ds1.test) + len(ds1.val)) * 2 == len(ds1)
