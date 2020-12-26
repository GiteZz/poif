from pathlib import Path

import boto3
from botocore.config import Config

from poif.project_interface.classes.location import DvcDataPoint


def s3_download_file(s3_config: S3Config, dvc_datapoint: DvcDataPoint, dest_file: Path) -> None:
    dataset_sess = boto3.session.Session(profile_name=s3_config.profile)
    s3 = dataset_sess.resource('s3',
                               endpoint_url=s3_config.endpointurl,
                               config=Config(signature_version='s3v4')
                               )
    file_name = f'{s3_config.folder}/{dvc_datapoint.data_tag[:2]}/{dvc_datapoint.data_tag[2:]}'

    s3.Bucket(f'{s3_config.bucket}').download_file(file_name, str(dest_file))


def s3_get_object_size(s3_config: S3Config, dvc_datapoint: DvcDataPoint) -> int:
    dataset_sess = boto3.session.Session(profile_name=s3_config.profile)
    s3 = dataset_sess.resource('s3',
                               endpoint_url=s3_config.endpointurl,
                               config=Config(signature_version='s3v4')
                               )
    file_name = f'{s3_config.folder}/{dvc_datapoint.data_tag[:2]}/{dvc_datapoint.data_tag[2:]}'

    size = s3.Bucket(f'{s3_config.bucket}').lookup(file_name).size

    return size