from poif.config.remote.base import RemoteConfig, RemoteType, S3Config
from poif.tests import get_temp_file


def test_read_write():
    file_loc = get_temp_file()

    s3_config = S3Config(url="http://google.be", profile="profile", bucket="bucket")
    remote_config = RemoteConfig(
        remote_type=RemoteType.S3, data_folder="data", config=s3_config
    )

    remote_config.write(file_loc)

    loaded_config = RemoteConfig.read(file_loc)

    assert loaded_config == remote_config
