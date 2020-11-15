import yaml
from typing import List, Optional
from pathlib import Path
from dataclasses import dataclass, field


config_folder = Path.home() / '.daif'
config_folder.mkdir(exist_ok=True)

config_file = config_folder / 'config.yaml'


def get_config_content() -> Optional['DaifConfig']:
    if config_file.exists():
        with open(config_file, 'r') as f:
            current_config = yaml.safe_load(f)

        if type(current_config) == dict and set(current_config.keys()) == {'origins', 'current_origin'}:
            selected_origin = None
            origin_list = []
            for origin_dict in current_config['origins']:
                origin = OriginConfig(**origin_dict)
                origin_list.append(origin)
                if origin.name == current_config['current_origin']:
                    selected_origin = origin

            return DaifConfig(current_origin=selected_origin, origins=origin_list)

    # Config file does not comply with the expected format. Therefore a new one is
    new_config = DaifConfig()
    new_config.save()

    return new_config


@dataclass
class DatasetConfig:
    s3_bucket: str
    s3_endpoint: str
    dataset_name: str
    data_folders: List[str]
    git_remote_url: str

    def get_data_folders(self):
        return [Path.cwd() / folder for folder in self.data_folders]

@dataclass
class DaifConfig:
    current_origin: Optional['OriginConfig'] = None
    origins: Optional[List['OriginConfig']] = field(default_factory=list)

    def save(self):
        yaml_dict = {
            'current_origin': self.current_origin.name if self.current_origin is not None else None,
            'origins': [vars(origin) for origin in self.origins] if self.origins is not None else None
        }
        with open(config_file, 'w') as f:
            yaml.safe_dump(yaml_dict, f)


@dataclass
class OriginConfig:
    name: str
    git_url: Optional[str] = None
    git_api_key: Optional[str] = None
    s3_profile: Optional[str] = None
    s3_default_bucket: Optional[str] = None
    s3_default_endpoint: Optional[str] = None

