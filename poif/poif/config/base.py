from pathlib import Path
from typing import Set

from pydantic import BaseModel

from poif.config import poif_config_folder


class Config(BaseModel):
    @classmethod
    def read(cls, file: Path):
        with open(file, 'r') as f:
            json_content = f.read()
        return cls.parse_raw(json_content)

    def write(self, file: Path):
        with open(file, 'w') as f:
            f.write(self.json())

    @classmethod
    def get_default(cls):
        if cls.default_location is not None and cls.default_location().is_file():
            return cls.read(cls.default_location())

        return None

    def json(self, *args, **kwargs) -> str:
        kwargs['exclude'] = self.get_write_exclusions()
        return super().json(*args, **kwargs)

    @classmethod
    def default_location(cls) -> Path:
        return poif_config_folder / cls.get_default_name()

    @classmethod
    def get_default_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_write_exclusions(cls) -> Set[str]:
        return {'default_location'}