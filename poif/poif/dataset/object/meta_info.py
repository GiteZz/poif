from typing import List, Optional, Union


class MetaInfoMixin:
    def __init__(self):
        super().__init__()
        self.label: Optional[Union[str, int]] = None
        self.tags: List[str] = []
