from pathlib import Path
from typing import Dict, List, Optional, Union

FileHash = str
RelFilePath = str
DatasetType = str  # train, test, val, ...

URL = str
UrlParams = Dict[str, str]

ZeroOrMorePaths = Optional[Union[Path, List[Path]]]