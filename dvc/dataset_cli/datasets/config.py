from datasets.tools.git import get_existing_credentials, add_git_credential
from datasets.tools import yes
import getpass
import datasets.tools.config_file as config_file


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


def config_new_origin_collect_options():
    options = {}
    print("Origin name:")
    options['name'] = input()
    print("Git URL: [format: http(s)://domain.org]")
    options['git_url'] = input()
    git_url_without_http = options['git_url'].split('/')[-1]
    print("Git API key: [Only needed when new datasets are created, leave blank if that is not needed]")
    options['git_api_key'] = input()

    existing_git_cred_urls = get_existing_credentials()
    if git_url_without_http not in existing_git_cred_urls:
        print(f'{git_url_without_http} credentials are currently not stored on the pc. Would you like to do that? [y:n]')
        if yes():
            print('Username:')
            options['new_git_username'] = input()
            options['new_git_password'] = getpass.getpass('Password:')

    # TODO Change for different ways of configuring s3 bucket -> one url or bucket + endpoint
    print("Default S3 bucket: [Leave blank if configured different for each dataset]")
    options['s3_bucket_name'] = input()
    print("Default S3 endpoint: [Leave blank if configured different for each dataset]")
    options['s3_endpoint'] = input()
    print("Use existing S3 profile?")
    options['use_existing_s3_profile'] = yes()
    if options['use_existing_s3_profile']:
        options['s3_profile_name'] = input()
    else:
        raise NotImplementedError()
        # print("Create S3 profile?")
        # options['new_s3_profile'] = yes()
        # if options['new_s3_profile']:

    print("Set as current origin?")
    options['set_as_current'] = yes()

    return options


def config_new_origin(args):
    options = config_new_origin_collect_options()
    if 'new_git_username' in options:
        add_git_credential(options['new_git_username'], options['new_git_password'], options['git_url'])
    current_config = config_file.get_config_content()

    # TODO S3 profile is obligated atm
    new_origin = {
        'name': options['name'],
        'git_url': options['git_url'],
        'git_api_key': options['git_api_key'],
        'default_s3_bucket': options['s3_bucket_name'],
        'default_s3_endpoint': options['s3_endpoint'],
        's3_profile': options['s3_profile_name']
    }

    if type(current_config['origins']) == list:
        current_config['origins'].append(new_origin)
    else:
        current_config['origins'] = [new_origin]

    if options['set_as_current']:
        current_config['current_origin'] = options['name']

    config_file.save_new_config(current_config)


def config_set(args):
    pass

def config_delete(args):
    pass