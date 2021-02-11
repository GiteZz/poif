from dataclasses import dataclass, field
from typing import List


class MetaInfoMixin:
    def __init__(self, label: str = None, tags: List[str] = None):
        self.label = label
        self.tags = [] if tags is None else tags
