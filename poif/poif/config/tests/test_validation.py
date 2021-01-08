import pytest
from pydantic import ValidationError

from poif.config import ReadmeConfig, RemoteConfig, S3Config
from poif.tests import MonkeyPatchSequence


def test_s3():
    a = S3Config(url='http://google.com', profile='profile', bucket='bucket')
    with pytest.raises(ValidationError):
        b = S3Config(url='url', profile='profile', bucket='bucket')



