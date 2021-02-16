from typing import List, Optional


class MetaInfoMixin:
    def __init__(self):
        super().__init__()
        self.label: Optional[str] = None
        self.tags: List[str] = []
