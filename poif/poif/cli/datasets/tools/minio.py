import tempfile
from pathlib import Path
from typing import List, Tuple

import boto3
import cv2
from botocore.client import Config

from poif.cli.datasets.tools.config import DatasetConfig
from poif.data.remote.s3 import S3Remote

new_height = 256


def upload_datasets_images(s3_config: S3Remote, files: List[Tuple[Path, Path]]):
    # TODO upload with remote
    print(f'uploading {len(files)} files for readme')
    dataset_sess = boto3.session.Session(profile_name=s3_config.profile)
    s3 = dataset_sess.resource('s3',
                               endpoint_url=s3_config.endpoint,
                               config=Config(signature_version='s3v4')
                               )
    # Rescale the images
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir_path = Path(tmpdirname)

        for or_file, dest_file in files:
            or_img = cv2.imread(str(or_file), cv2.IMREAD_UNCHANGED)
            or_height, or_width = or_img.shape[0], or_img.shape[1]

            scale_factor = new_height / or_height # percent of original size
            width = int(or_width * scale_factor)
            height = int(or_height * scale_factor)
            new_dim = (width, height)
            # resize image
            resized_img = cv2.resize(or_img, new_dim, interpolation=cv2.INTER_AREA)

            or_img_name = or_file.parts[-1]
            new_name = temp_dir_path / or_img_name
            cv2.imwrite(str(new_name), resized_img)

            s3.Bucket(f'{s3_config.bucket}').upload_file(str(new_name), str(dest_file))

