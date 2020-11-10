from datasets.git_tools import get_existing_credentials, add_git_credential
from datasets.tools import yes
import getpass

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

def config_new_origin(args):
    print("Origin name:")
    name = input()
    print("Git URL: [format: http(s)://domain.org]")
    git_url = input()
    git_url_without_http = git_url.split('/')[-1]
    print("Git API key: [Only needed when new datasets are created, leave blank if that is not needed]")
    git_api_key = input()

    existing_git_cred_urls = get_existing_credentials()

    if git_url_without_http not in existing_git_cred_urls:
        print(f'{git_url_without_http} credentials are currently not stored on the pc. Would you like to do that? [y:n]')
        if yes():
            print('Username:')
            username = input()
            print('Password:')
            password = getpass.getpass()
            add_git_credential(username, password, git_url)






def config_set(args):
    pass

def config_delete(args):
    pass