import pytest
from pydantic import ValidationError

from poif.config.remote.s3 import S3Config


def test_s3():
    a = S3Config(url="http://google.com", profile="profile", bucket="bucket")
    with pytest.raises(ValidationError):
        b = S3Config(url="url", profile="profile", bucket="bucket")
