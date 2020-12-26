import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import cv2
import pytest

from poif.data.access.datapoint import DvcDataPoint
from poif.data.access.origin import DvcOrigin
from poif.data.cache.disk import LocalCache
from poif.data.remote.base import Remote
from poif.tests import assert_image_nearly_equal, get_img
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
        temp_file = Path(tempfile.mkstemp()[1] + '.jpg')
        img = files[file_location.data_tag]
        bgr_to_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(temp_file), bgr_to_rgb)
        shutil.copy(str(temp_file), str(save_path))

        self.files_downloaded += 1

    def get_object_size(self, file_location: DvcDataPoint):
        return file_sizes[file_location.data_tag]


class MockOrigin(DvcOrigin):
    remote = None
    @property
    def dataset_tag(self):
        return 'dataset'

    @property
    def origin_tag(self):
        return 'origin'

    def get_tag_file_mapping(self) -> Dict[FileHash, RelFilePath]:
        return tag_file_mapping

    def get_remote(self) -> Remote:
        if self.remote is None:
            self.remote = MockRemote()
        return self.remote


@dataclass
class MockDataPoint(MockOrigin):
    data_tag: str


@pytest.fixture
def dvc_origin():
    return MockOrigin(git_commit='commit', git_url='url')


def test_get_dataset_info(dvc_origin):
    cache_work_dir = Path(tempfile.mkdtemp())
    cache = LocalCache(work_dir=cache_work_dir)

    cache_tag_to_files = cache.get_files(dvc_origin)
    assert cache_tag_to_files == tag_file_mapping

    for _ in range(2):
        for data_tag, or_name in cache_tag_to_files.items():
            img_from_cache = cache.get_file(MockDataPoint(git_url=dvc_origin.git_url,
                                                         git_commit=dvc_origin.git_commit,
                                                         data_tag=data_tag)
                                            )
            assert_image_nearly_equal(files[data_tag], img_from_cache)
    assert dvc_origin.remote.files_downloaded == 4