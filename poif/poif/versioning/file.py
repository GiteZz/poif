import json
from pathlib import Path

from poif.tagged_data import DiskData
from poif.typing import FileHash
from poif.utils import get_file_name_from_path, get_relative_path


class VersionedFile(DiskData):
    base_dir: Path
    file_path: Path

    def __init__(self, base_dir: Path, file_path: Path, tag: FileHash = None):
        relative_path = get_relative_path(base_dir, file_path)
        super().__init__(file_path, relative_path, tag=tag)

    def get_vfile_name(self):
        file_name = get_file_name_from_path(self.file_path)

        return f"{file_name}.vfile"

    def write_vfile_to_folder(self, directory: Path) -> Path:
        vfile = directory / self.get_vfile_name()
        with open(vfile, "w") as f:
            json.dump({"path": self.relative_path, "tag": self.tag}, f, indent=4)

        return vfile

    @staticmethod
    def from_file(vfile: Path, base_dir: Path) -> "VersionedFile":
        with open(vfile) as f:
            file_content = json.load(f)
        file_path = base_dir / file_content["path"]
        return VersionedFile(
            base_dir=base_dir, file_path=file_path, tag=file_content["tag"]
        )
