from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any


class Parser(ABC):
    @staticmethod
    @abstractmethod
    def parse(bytes: BytesIO) -> Any:
        pass