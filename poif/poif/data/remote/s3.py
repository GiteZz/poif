
import typing
from dataclasses import dataclass, field
from pathlib import Path

import boto3
from botocore.config import Config

from poif.data.remote.base import FileRemote
from poif.data.repo.file_remote import FileRemoteTaggedRepo

if typing.TYPE_CHECKING:
    from poif.config.remote import S3Config
    from poif.data.datapoint.base import TaggedData


@dataclass
class S3Remote(FileRemote):
    def __init__(self, config: 'S3Config'):
        self.config = config

    def get_session(self):
        dataset_sess = boto3.session.Session(profile_name=self.config.profile)
        return dataset_sess.resource('s3',
                                     endpoint_url=self.config.url,
                                     config=Config(signature_version='s3v4')
                                     )

    def download(self, file_name: str) -> bytes:
        response = self.get_bucket().get_object(file_name)
        return response['body'].read()

    def upload(self, source: bytes, remote_dest: str):
        # TODO probably doesn't work
        self.get_bucket().put_object(Body=source, Key=remote_dest)

    def get_bucket(self):
        return self.get_session().Bucket(f'{self.config.bucket}')

    def get_object_size(self, file_name: str) -> int:
        size = self.get_bucket().lookup(file_name).size

        return size

    def upload_file(self, source: Path, dest: str):
        self.get_bucket().upload_file(str(source), dest)


@dataclass
class TaggedS3(FileRemoteTaggedRepo):
    s3_config: 'S3Config'
    s3_remote: S3Remote = field(init=False)

    def __post_init__(self):
        self.s3_remote = S3Remote(config=self.s3_config)

    def get_remote_name(self, data: 'TaggedData'):
        return f'{self.data_folder}/{data.tag[:2]}/{data.tag[2:]}'

    def download(self, data: 'TaggedData') -> bytes:
        return self.s3_remote.download(self.get_remote_name(data))

    def get_object_size(self, data: 'TaggedData'):
        return self.s3_remote.get_object_size(self.get_remote_name(data))

    def upload(self, data: 'TaggedData'):
        return self.s3_remote.upload(data.get(), self.get_remote_name(data))

# TODO finish
# class TaggedHttp(TaggedRemote):
#     git_url: str
#     git_commit: str
#
#     def get_url_params(self, data: TaggedData):
