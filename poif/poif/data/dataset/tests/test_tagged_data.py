from poif.data.datapoint.base import TaggedData
from typing import Any, List, Dict

from poif.data.dataset.tagged_data import TaggedDataDataset
from poif.data.transform.combine import CombineByTemplate
from poif.tests import get_img


from typing import List, Optional, Union

import pytest


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
    sub_datasets = ['train', 'val', 'test']
    labels = [f'cat{i}' for i in range(amount_categories)]

    for sub_dataset in sub_datasets:
        for label in labels:
            data_points.extend(
                [MockTaggedData(f'{sub_dataset}/{label}/rgb_{i}.jpg', get_img())
                 for i in range(imgs_per_set)]
            )
            data_points.extend(
                [MockTaggedData(f'{sub_dataset}/{label}/bw_{i}.jpg', get_img())
                 for i in range(imgs_per_set)]
            )

    return data_points


@pytest.fixture
def mask_dataset(imgs_per_set=10, sub_datasets=None) -> List[TaggedData]:
    if sub_datasets is None:
        sub_datasets = ['train', 'val', 'test']
    data_points = []

    for sub_dataset in sub_datasets:
        data_points.extend([MockTaggedData(f'{sub_dataset}/mask_{i}.jpg', get_img()) for i in range(imgs_per_set)])
        data_points.extend([MockTaggedData(f'{sub_dataset}/image_{i}.jpg', get_img()) for i in range(imgs_per_set)])

    return data_points


def test_combining_mask_img(mask_dataset):
    operation_list = [
        CombineByTemplate({'image': '*/mask*', 'mask': '*/mask*.jpg'})
    ]

    ds = TaggedDataDataset(operations=operation_list)
    ds.form(mask_dataset)

    assert len(mask_dataset) // 2 == len(ds)

