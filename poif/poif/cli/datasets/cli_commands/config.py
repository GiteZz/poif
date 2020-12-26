from typing import Tuple

import poif.data_interface.tools.config as config_tools
from poif.cli.datasets.tools.cli import (s3_input, yes_with_question)
from poif.data_interface.tools.config import DaifConfig


def config(args):
    command = args[0]
    valid_commands = {
        'new': config_new,
        'set': config_set,
        'delete': config_delete
    }

    if command in valid_commands.keys():
        valid_commands[command](args[1:])
    else:
        print(f'Please provide a config valid command. Valid commands are: {valid_commands.keys()}')


def config_new(args):
    command = args[0]
    valid_commands = {
        'origin': config_new_origin,
    }
    if command in valid_commands.keys():
        valid_commands[command](args[1:])
    else:
        print(f'Please provide a config valid command. Valid commands are: {valid_commands.keys()}')


def config_new_origin_collect_options() -> Tuple[config_tools.OriginConfig, bool]:
    new_origin_dict = {}
    print("Origin name:")
    new_origin_dict['name'] = input()

    if yes_with_question('Do you want to create repos automatically? [Currently only gitlab is supported]'):
        print("Git URL: [format: http(s)://domain.org]")
        new_origin_dict['git_url'] = input()

        print("Git API key:")
        new_origin_dict['git_api_key'] = input()

    if yes_with_question('Do you want to set default S3 properties?'):
        new_origin_dict['default_s3'] = s3_input(default_bucket='datasets')

    set_current = yes_with_question('Set as current origin?')

    return config_tools.OriginConfig(**new_origin_dict), set_current


def config_new_origin(args):
    current_config = DaifConfig.load()
    origin_config, set_as_current = config_new_origin_collect_options()
    current_config.origins.append(origin_config)
    if set_as_current:
        current_config.current_origin = origin_config

    current_config.save()


def config_set(args):
    pass


def config_delete(args):
    pass