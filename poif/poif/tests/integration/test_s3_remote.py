from poif.data.remote.s3 import S3Remote
from poif.tests import get_img_file
from poif.tests.integration.minio.config import MinioConfig
from poif.tests.integration.minio.setup import minio_setup, get_remote_from_config

import uuid

def setup_and_get_remote():
    minio_config = MinioConfig()
    minio_setup(minio_config)

    return get_remote_from_config(minio_config)

def test_s3_remote():
    s3_remote = setup_and_get_remote()
    img = get_img_file()

    with open(img, 'rb') as f:
        file_bytes = f.read()

    remote_name = str(uuid.uuid4())
    s3_remote.upload(file_bytes, remote_name)
    remote_size = s3_remote.get_object_size(remote_name)
    assert remote_size == len(file_bytes)

    remote_bytes = s3_remote.download(remote_name)
    assert remote_bytes == file_bytes