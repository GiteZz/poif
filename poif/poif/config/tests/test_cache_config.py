from poif.config import CacheConfig
from pathlib import Path

from poif.tests import get_temp_file


def test_read_write():
    file_loc = get_temp_file()

    config = CacheConfig(enable=True,
                         data_storage_location=Path.cwd() / 'data',
                         git_storage_location=Path.cwd() / 'data',
                         cache_uploads=True
                         )

    config.write(file_loc)

    loaded_config = CacheConfig.read(file_loc)

    assert loaded_config == config
