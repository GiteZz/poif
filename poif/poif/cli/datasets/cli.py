import sys

from poif.data_interface.cli_commands.config import config
from poif.data_interface.cli_commands.create import create
from poif.data_interface.cli_commands.get import get
from poif.data_interface.cli_commands.init import init
from poif.data_interface.cli_commands.push import push
from poif.data_interface.cli_commands.update import update


def main():
    args = sys.argv
    print(args)
    if len(args) <= 1:
        print(f'Please provide a command.')

    command = args[1]
    valid_commands = {
        'init': init,
        'config': config,
        'get': get,
        'update': update,
        'push': push,
        'create': create
    }
    if command in valid_commands.keys():
        valid_commands[command](args[2:])
    else:
        print(f'Please provide a valid command. Valid commands are: {valid_commands.keys()}')
