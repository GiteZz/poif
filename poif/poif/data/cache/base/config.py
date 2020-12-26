import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from dataclasses_json import dataclass_json

from poif.data.remote.base import Remote
from poif.typing import FileHash, RelFilePath


@dataclass_json
@dataclass
class DatasetInfo:
    files: Dict[FileHash, RelFilePath]
    remote: Remote

    def save(self, file: Path):
        with open(file, 'w') as f:
            json.dump(self.to_dict(), f)

    @staticmethod
    def load(file: Path) -> 'DatasetInfo':
        with open(file, 'r') as f:
            ds_info_dict = json.load(f)
        return DatasetInfo.from_dict(ds_info_dict)


