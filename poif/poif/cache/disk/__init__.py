from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from poif.cache.base import DatasetInfo
from poif.typing import FileHash


@dataclass
class CacheConfig:
    work_dir: Path

    config_folder: Path = field(init=False)
    ds_info_cache: Path = field(init=False)
    git_folder: Path = field(init=False)
    data_folder: Path = field(init=False)

    cached_ds_info: Dict[FileHash, DatasetInfo] = field(default_factory=dict)

    def __post_init__(self):
        # Folder initiation
        self.config_folder = self.work_dir / "config"
        self.ds_info_cache = self.work_dir / "ds_info"
        self.git_folder = self.work_dir / "git_repos"
        self.data_folder = self.work_dir / "data"

        self.work_dir.mkdir(exist_ok=True)
        self.config_folder.mkdir(exist_ok=True)
        self.ds_info_cache.mkdir(exist_ok=True)
        self.git_folder.mkdir(exist_ok=True)
        self.data_folder.mkdir(exist_ok=True)

        # Reload previous configs
        for file in self.ds_info_cache.glob("*.json"):
            ds_info = DatasetInfo.load(file)
            ds_id = file.parts[-1].replace(".json", "")
            self.cached_ds_info[ds_id] = ds_info
