import unittest
from dataclasses import dataclass
from enum import Enum

from dataclasses_json import dataclass_json


def test_enum_serialization():
    from enum import Enum

    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    @dataclass_json
    @dataclass
    class ClassWithEnum:
        color: Color
        value: str

    test_class = ClassWithEnum(color=Color.GREEN, value="test")
    class_dict = test_class.to_dict()
    class_from_dict = ClassWithEnum.from_dict(class_dict)

    assert test_class.color == class_from_dict.color
    assert test_class.value == class_from_dict.value


