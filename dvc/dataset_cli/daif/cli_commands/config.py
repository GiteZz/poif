from daif.tools.git import get_existing_credentials, add_git_credential
from daif.tools import yes, yes_with_question, simple_input
import getpass
import daif.tools.config as config_tools
from typing import Tuple


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

    if yes_with_question('Do you want to set a default S3 profile?'):
        print('Profile name:')
        new_origin_dict['s3_profile'] = input()

    if yes_with_question('Do you want to set a default bucket and endpoint?'):
        print('Profile name:')
        new_origin_dict['s3_default_bucket'] = simple_input('Default S3 bucket', value_when_empty='datasets')
        new_origin_dict['s3_default_endpoint'] = simple_input('Default S3 endpoint', use_empy_value=False)

    set_current = yes_with_question('Set as current origin?')

    return config_tools.OriginConfig(**new_origin_dict), set_current


def config_new_origin(args):
    current_config = config_tools.get_config_content()
    origin_config, set_as_current = config_new_origin_collect_options()
    current_config.origins.append(origin_config)
    if set_as_current:
        current_config.current_origin = origin_config

    config_tools.save_config(current_config)


def config_set(args):
    pass


def config_delete(args):
    pass