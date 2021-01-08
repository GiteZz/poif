import json
from typing import List

import boto3
import botocore.exceptions
import docker
from botocore.config import Config

from poif.tests.integration.gitlab.wait import is_alive, wait_on_url
from poif.tests.integration.minio.config import MinioConfig


def get_s3_resource(config: MinioConfig):
    dataset_sess = boto3.session.Session(profile_name=config.profile)
    return dataset_sess.resource('s3',
                               endpoint_url=f'http://localhost:{config.port}',
                               config=Config(signature_version='s3v4')
                               )


def create_buckets(config: MinioConfig, bucket_names: List[str]):
    s3 = get_s3_resource(config)

    for bucket_name in bucket_names:
        try:
            s3.create_bucket(Bucket=bucket_name)
        except Exception as e:
            if not e.response['Error']['Code'] == "BucketAlreadyOwnedByYou":
                raise e


def set_public(config: MinioConfig, bucket_names: List[str]):
    s3 = get_s3_resource(config)

    for bucket in bucket_names:
        existing_policy = s3.BucketPolicy(bucket)

        policy = {
            "Statement": [
                {
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            "*"
                        ]
                    },
                    "Resource": [
                        f'arn:aws:s3:::{bucket}/*'
                    ]
                }
            ],
            "Version": "2012-10-17"
        }

        existing_policy.put(Policy=json.dumps(policy))
