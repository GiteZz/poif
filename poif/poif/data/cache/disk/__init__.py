import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from poif.data.cache.base import DvcCache
from poif.data.cache.base import DatasetInfo
from poif.project_interface.classes.data_location import DvcDataPoint, DvcOrigin
from poif.typing import FileHash, RelFilePath


@dataclass
class LocalCache(DvcCache):
    work_dir: Path

    config_folder: Path = field(init=False)
    ds_info_cache: Path = field(init=False)
    git_folder: Path = field(init=False)
    data_folder: Path = field(init=False)

    cached_ds_info: Dict[FileHash, DatasetInfo] = field(init=False)

    def __post_init__(self):
        # Folder initiation
        self.config_folder = self.work_dir / 'config'
        self.ds_info_cache = self.work_dir / 'ds_info'
        self.git_folder = self.work_dir / 'git_repos'
        self.data_folder = self.work_dir / 'data'

        self.work_dir.mkdir(exist_ok=True)
        self.config_folder.mkdir(exist_ok=True)
        self.ds_info_cache.mkdir(exist_ok=True)
        self.git_folder.mkdir(exist_ok=True)
        self.data_folder.mkdir(exist_ok=True)

        # Reload previous configs
        for file in self.ds_info_cache.glob('*.json'):
            ds_info = DatasetInfo.load(file)
            ds_id = file.parts[-1].replace('.json', '')
            self.cached_ds_info[ds_id] = ds_info

    def get_dataset_info(self, dvc_origin: DvcOrigin) -> DatasetInfo:
        # Check if info is not already loaded
        if dvc_origin.origin_tag in self.cached_ds_info:
            return self.cached_ds_info[dvc_origin.origin_tag]

        ds_info_json = self.ds_info_cache / f'{dvc_origin.origin_tag}.json'
        if ds_info_json.exists():
            ds_info = DatasetInfo.load(ds_info_json)
            self.cached_ds_info[dvc_origin.origin_tag] = ds_info
            return ds_info

        new_ds_info = DatasetInfo(files=dvc_origin.get_tag_file_mapping(), remote=dvc_origin.get_remote())
        new_ds_info.save(self.ds_info_cache / f'{dvc_origin.origin_tag}.json')
        self.cached_ds_info[dvc_origin.origin_tag] = new_ds_info
        return new_ds_info

    def get_files(self, dvc_origin: DvcOrigin) -> Dict[FileHash, RelFilePath]:
        ds_info = self.get_dataset_info(dvc_origin)

        return ds_info.files

    def get_extension(self, file_location: DvcDataPoint):
        ds_info = self.get_dataset_info(file_location)
        original_file_path = ds_info.files[file_location.data_tag]
        file_name = Path(original_file_path).parts[-1]
        extension = file_name.split('.')[-1]

        return extension

    def get_file(self, file_location: DvcDataPoint):
        hash_file_path = self.get_file_path(file_location)

        extension = self.get_extension(file_location)

        with open(hash_file_path, 'rb') as f:
            file_bytes = f.read()

        return self.parse_file(file_bytes, extension)

    def get_file_size(self, file_location: DvcDataPoint) -> int:
        # TODO fix duplication
        dataset_id = LocalCache.git_to_tag(file_location)
        file_path = self.data_folder / dataset_id / file_location.data_tag
        if file_path.is_file():
            return os.path.getsize(file_path)

        ds_info = self.get_dataset_info(file_location)
        return ds_info.remote.get_object_size(file_location)

    def get_file_path(self, file_location: DvcDataPoint) -> Path:
        """
        Files are saved under their hash and not under their original filename
        """
        dataset_id = LocalCache.git_to_tag(file_location)
        file_path = self.data_folder / dataset_id / file_location.data_tag
        if file_path.is_file():
            return file_path

        ds_info = self.get_dataset_info(file_location)

        ds_info.remote.download_file(file_location, file_path)

        return file_path
