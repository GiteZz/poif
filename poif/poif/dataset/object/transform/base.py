from abc import ABC, abstractmethod
from typing import Any, Type


class DataTransform(ABC):
    supported_type: Type

    @abstractmethod
    def transform(self, input_object: Any) -> Any:
        pass

    def __call__(self, input_object: Any) -> Any:
        assert isinstance(input_object, self.supported_type)
        return self.transform(input_object)

    @abstractmethod
    def get_tag(self) -> str:
        pass

    @property
    def tag(self) -> str:
        return self.get_tag()
