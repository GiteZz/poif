from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict, Set
from pathlib import Path
import json
from poif.typing import FileHash, RelFilePath




@dataclass_json
@dataclass
class S3Config:
    url: str
    endpointurl: str
    profile: str

    bucket: str = field(init=False)
    folder: str = field(init=False)

    def __post_init__(self):
        url_no_URI = self.url.replace('s3://', '')
        self.bucket, self.folder = url_no_URI.split('/')


@dataclass_json
@dataclass
class DatasetInfo:
    files: Dict[FileHash, RelFilePath]
    s3_config: S3Config

    def save(self, file: Path):
        with open(file, 'w') as f:
            json.dump(self.to_dict(), f)

    @staticmethod
    def load(file: Path) -> 'DatasetInfo':
        with open(file, 'r') as f:
            ds_info_dict = json.load(f)
        return DatasetInfo.from_dict(ds_info_dict)


