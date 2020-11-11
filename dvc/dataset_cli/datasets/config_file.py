import pathlib
import yaml

config_folder = pathlib.Path.home() / '.datasets'
config_folder.mkdir(exist_ok=True)

config_file = config_folder / 'config.yml'


def get_new_config_file():
    return {'current_origin': None, 'origins': None}


def save_new_config(new_config):
    with open(config_file, 'w') as f:
        yaml.safe_dump(new_config, f)


def get_config_content():
    with open(config_file, 'r') as f:
        current_config = yaml.safe_load(f)

    if type(current_config) == dict and set(current_config.keys()) == {'origins', 'current_origin'}:
        return current_config

    # Config file does not comply with the expected format. Therefore a new one is
    new_config_file = get_new_config_file()
    save_new_config(new_config_file)

    return new_config_file


def get_current_origin():
    config_content = get_config_content()

    if config_content['origins'] is None or config_content['current_origin'] is None:
        return None

    for origin in config_content['origins']:
        if origin['name'] == config_content['current_origin']:
            return origin

    return None
