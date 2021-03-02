from abc import ABC, abstractmethod
from typing import Any, List


class Parser(ABC):
    approved_extensions: List[str]

    @staticmethod
    @abstractmethod
    def parse(to_parse: bytes) -> Any:
        pass
