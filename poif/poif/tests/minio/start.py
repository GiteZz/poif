from typing import List

import boto3
import docker
from botocore.config import Config
import json
from poif.tests.gitlab.wait import wait_on_url, is_alive


class MinioConfig:
    port = 9000
    access_key = 'minio'
    secret_key = 'minio123'

class MinioDockerConfig:
    image = 'minio/minio'
    name = 'minio'
    envs = {
        'MINIO_ACCESS_KEY': MinioConfig.access_key,
        'MINIO_SECRET_KEY': MinioConfig.secret_key
    }
    ports = {
        '9000': MinioConfig.port
    }
    restart_if_active = True
    command = 'server /data'
    commands = [
        'gitlab-rails runner "token = User.find_by_username(\'root\').personal_access_tokens.create(scopes: [:api], name: \'Automation token\');token.set_token(\'root-api-key\');token.save!"'
    ]

def get_s3_resource():
    dataset_sess = boto3.session.Session(profile_name='datasets')
    return dataset_sess.resource('s3',
                               endpoint_url='http://localhost:9000',
                               config=Config(signature_version='s3v4')
                               )

def create_buckets(bucket_names: List[str]):
    s3 = get_s3_resource()

    for bucket_name in bucket_names:
        s3.create_bucket(Bucket=bucket_name)


def set_public(bucket_names: List[str]):
    public_policy = open('./policy.json', 'r').read()
    s3 = get_s3_resource()

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


minio_url = 'http://localhost:9000'

if not is_alive(minio_url):
    client = docker.from_env()

    client.containers.run(image=MinioDockerConfig.image,
                          environment=MinioDockerConfig.envs,
                          ports=MinioDockerConfig.ports,
                          name=MinioDockerConfig.name,
                          command=MinioDockerConfig.command,
                          detach=True
                          )

    wait_on_url(minio_url, interval=2)

    create_buckets(['datasets', 'readme-images'])
    set_public(['readme-images'])
