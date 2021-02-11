import json
from abc import ABC, abstractmethod
from hashlib import md5
from pathlib import Path
from typing import List, Optional

from tqdm import tqdm

from poif.tagged_data.base import LazyLoadedTaggedData
from poif.typing import FileHash
from poif.utils import RecursiveFileIterator, get_relative_path
from poif.versioning.file import VersionedFile


class Mapping(LazyLoadedTaggedData, ABC):
    def __init__(self):
        super().__init__(relative_path="")
        self._mapping = None

    @property
    def size(self) -> int:
        return len(self.get())

    @property
    def extension(self) -> str:
        return "mapping"

    def get(self) -> bytes:
        return json.dumps(self.mapping).encode("utf-8")

    @property
    def mapping(self):
        if self._mapping is None:
            self.set_mapping()
        return self._mapping

    def set_tag(self):
        self._tag = self.get_mapping_hash()

    def get_mapping_hash(self):
        # Sort the files (Can't be sure that the file system gives them in order)
        sorted_tags = self.get_sorted_mapping()
        intermediate_hash = md5()

        for tag in sorted_tags:
            intermediate_hash.update(tag.encode("utf-8"))

        return intermediate_hash.hexdigest()

    def get_sorted_mapping(self) -> List[FileHash]:
        tags = list(self.mapping.keys())
        relative_files = list(self.mapping.values())

        return [tag for _, tag in sorted(zip(relative_files, tags), key=lambda pair: pair[0])]

    @abstractmethod
    def set_mapping(self):
        pass


class VersionedDirectory(Mapping):
    base_dir: Path
    data_dir: Optional[Path] = None

    _files: Optional[List[VersionedFile]] = None

    def __init__(self, base_dir: Path, data_dir: Path, tag=None):
        super().__init__()

        self.base_dir = base_dir
        self.data_dir = data_dir

    @property
    def files(self):
        if self._files is None:
            self.set_files()
        return self._files

    def set_mapping(self):
        self._mapping = {}
        for file in self.files:
            self._mapping[file.tag] = file.relative_path

    def set_files(self):
        self._files = []
        for file in tqdm(RecursiveFileIterator(self.data_dir)):
            versioned_file = VersionedFile(base_dir=self.base_dir, file_path=file)
            self._files.append(versioned_file)

    def write_vdir_to_folder(self, directory: Path) -> Path:
        vdir_file = directory / self.get_vdir_name()
        with open(vdir_file, "w") as f:
            json.dump(
                {
                    "data_folder": get_relative_path(self.base_dir, self.data_dir),
                    "tag": self.tag,
                },
                f,
                indent=4,
            )

        return vdir_file

    def get_vdir_name(self):
        file_name = self._get_file_name()

        return f"{file_name}.vdir"

    def _get_file_name(self):
        relative_path = get_relative_path(self.base_dir, self.data_dir)
        path_snake_case = relative_path.replace("/", "_")

        return path_snake_case

    @staticmethod
    def from_vdir_file(vdir_file: Path, base_dir: Path) -> "VersionedDirectory":
        with open(vdir_file, "r") as f:
            vdir_contents = json.load(f)

        tag = vdir_contents["tag"]
        data_dir = base_dir / vdir_contents["data_folder"]

        return VersionedDirectory(base_dir=base_dir, data_dir=data_dir, tag=tag)
