from dataclasses import dataclass, field
from pathlib import Path

import boto3
from botocore.config import Config
from dataclasses_json import dataclass_json

from poif.data.remote.base import Remote
from poif.typing import FileHash


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

    def get_session(self):
        dataset_sess = boto3.session.Session(profile_name=self.profile)
        return dataset_sess.resource('s3',
                                     endpoint_url=self.endpointurl,
                                     config=Config(signature_version='s3v4')
                                     )

    def get_bucket(self):
        return self.get_session().Bucket(f'{self.bucket}')

    def get_file(self, tag: FileHash) -> bytes:

        file_name = f'{self.folder}/{tag[:2]}/{tag[2:]}'

        response = self.get_bucket().get_object(file_name)
        return response['body'].read()

    def get_object_size(self, tag: FileHash) -> int:
        file_name = f'{self.folder}/{tag[:2]}/{tag[2:]}'

        size = self.get_bucket().lookup(file_name).size

        return size
