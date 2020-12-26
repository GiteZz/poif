import typing
from dataclasses import dataclass, field
from pathlib import Path

import boto3
from botocore.config import Config
from dataclasses_json import dataclass_json

from poif.data.remote.base import Remote

if typing.TYPE_CHECKING:
    from poif.data.access.datapoint import DvcDataPoint


@dataclass_json
@dataclass
class S3Remote(Remote):
    url: str
    endpointurl: str
    profile: str

    bucket: str = field(init=False)
    folder: str = field(init=False)

    def __post_init__(self):
        url_no_URI = self.url.replace('s3://', '')
        self.bucket, self.folder = url_no_URI.split('/')

    def download_file(self, dvc_datapoint: 'DvcDataPoint', dest_file: Path) -> None:
        dataset_sess = boto3.session.Session(profile_name=self.profile)
        s3 = dataset_sess.resource('s3',
                                   endpoint_url=self.endpointurl,
                                   config=Config(signature_version='s3v4')
                                   )
        file_name = f'{self.folder}/{dvc_datapoint.data_tag[:2]}/{dvc_datapoint.data_tag[2:]}'

        s3.Bucket(f'{self.bucket}').download_file(file_name, str(dest_file))

    def get_object_size(self, dvc_datapoint: 'DvcDataPoint') -> int:
        dataset_sess = boto3.session.Session(profile_name=self.profile)
        s3 = dataset_sess.resource('s3',
                                   endpoint_url=self.endpointurl,
                                   config=Config(signature_version='s3v4')
                                   )
        file_name = f'{self.folder}/{dvc_datapoint.data_tag[:2]}/{dvc_datapoint.data_tag[2:]}'

        size = s3.Bucket(f'{self.bucket}').lookup(file_name).size

        return size