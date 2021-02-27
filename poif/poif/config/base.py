import json
from dataclasses import dataclass
from pathlib import Path
from typing import Set

from dataclasses_json import dataclass_json

from poif.config import poif_config_folder


@dataclass_json
@dataclass
class Config:
    def __post_init__(self):
        super().__init__()

    @classmethod
    def read(cls, file: Path):
        with open(file, "r") as f:
            json_content = json.load(f)

        class_fields = cls.__annotations__
        for key, value in json_content.items():
            expected_type = class_fields[key]

            if expected_type == Path:
                json_content[key] = Path(value)
        return cls.from_dict(json_content)

    def write(self, file: Path):
        config_content = self.to_dict()
        for key in self.get_write_exclusions():
            config_content.pop(key, None)

        for key, value in config_content.items():
            if isinstance(value, Path):
                config_content[key] = str(value)
        with open(file, "w") as f:
            json.dump(config_content, f)

    @classmethod
    def get_default(cls):
        if cls.default_location is not None and cls.default_location().is_file():
            return cls.read(cls.default_location())

        return None

    def json(self, *args, **kwargs) -> str:
        kwargs["exclude"] = self.get_write_exclusions()
        return super().json(*args, **kwargs)

    def save_default(self):
        self.write(self.default_location())

    @classmethod
    def default_location(cls) -> Path:
        return poif_config_folder / cls.get_default_name()

    @classmethod
    def get_default_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_write_exclusions(cls) -> Set[str]:
        return {"default_location"}
