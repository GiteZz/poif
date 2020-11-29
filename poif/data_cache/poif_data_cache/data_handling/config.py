from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict, Set


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

FileHash: str
FileName: str


@dataclass_json
@dataclass
class DatasetInfo:
    dataset_id: str
    files: Dict[FileHash, FileName]
    s3_config: S3Config
    downloaded_files: Set