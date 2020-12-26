import tempfile
from pathlib import Path
from typing import Dict

import cv2
import pytest

from poif.data.access.datapoint import DvcDataPoint
from poif.data.access.origin import Origin
from poif.data.cache.base.remote import Remote
from poif.data.cache.disk import LocalCache
from poif.tests import get_img
from poif.typing import FileHash, RelFilePath

files = {
    'aa': get_img(),
    'bb': get_img(),
    'cc': get_img(),
    'dd': get_img(),
}

tag_file_mapping = {
    'aa': '/train/01.jpg',
    'bb': '/train/02.jpg',
    'cc': '/train/03.jpg',
    'dd': '/train/04.jpg',
}

file_sizes = {
    'aa': 1,
    'bb': 2,
    'cc': 3,
    'dd': 4,
}


class MockRemote(Remote):

    files = []
    files_downloaded = 0

    def download_file(self, file_location: DvcDataPoint, save_path: Path):
        img = files[file_location.data_tag]
        cv2.imwrite(str(save_path), img)

        self.files_downloaded += 1

    def get_object_size(self, file_location: DvcDataPoint):
        return file_sizes[file_location.data_tag]


class MockOrigin(Origin):
    @property
    def dataset_tag(self):
        return 'dataset'

    @property
    def origin_tag(self):
        return 'origin'

    def get_tag_file_mapping(self) -> Dict[FileHash, RelFilePath]:
        return tag_file_mapping

    def get_remote(self) -> Remote:
        return MockRemote()


@pytest.fixture
def dvc_origin():
    return MockOrigin()


def test_get_dataset_info(dvc_origin):
    cache_work_dir = Path(tempfile.mkdtemp())
    cache = LocalCache(cache_work_dir)

    dataset_info = cache.get_dataset_info(dvc_origin)