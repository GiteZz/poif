from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataQuery:
    query_type: int
    path: Path

class DataQueryType:
    FROM_DISK: 0
    DVC_GIT: 1


"""
Use cases:

from datasets import dogs_vs_cats

dogs_vs_cats.get_meta_files()
dogs_vs_cats.train.get_meta_files()
dogs_vs_cats.train[0] -> (data, meta_data)
"""

