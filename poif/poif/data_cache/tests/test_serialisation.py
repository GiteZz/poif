import unittest

from poif_data_cache.data_handling.config import S3Config, DatasetInfo
from pathlib import Path
import json


def test_dsinfo():
    s3_conf = S3Config(url='s3://datasets/pneunomia', endpointurl='http://10.10.138.91:30210/', profile='datasets')
    downloaded_files = {
        'jklmsdwmjklsfdq': Path('/tmp/1'),
        'qsdfqsdfqsdfdff': Path('/tmp/2')
    }
    files = {
        'jklmsdwmjklsfdq': Path('/tmp/1'),
        'qsdfqsdfqsdfdff': Path('/tmp/2'),
        'jklsfdqjklmsfdj': Path('/tmp/3')
    }
    ds_info = DatasetInfo(s3_config=s3_conf,
                          files=files
                          )

    a = ds_info.to_json()
    b = 3

if __name__ == "__main__":
    test_dsinfo()