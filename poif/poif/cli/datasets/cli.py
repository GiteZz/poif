import sys

from poif.cli.datasets.cli_commands.cleanup import cleanup
# from poif.cli.datasets.cli_commands.config import config
from poif.cli.datasets.cli_commands.init import init
from poif.cli.datasets.cli_commands.update import update


def main():
    args = sys.argv
    if len(args) <= 1:
        print(f'Please provide a command.')

    command = args[1]
    valid_commands = {
        'init': init,
        # 'config': config,
        'update': update,
        'cleanup': cleanup
    }
    if command in valid_commands.keys():
        valid_commands[command](args[2:])
    else:
        print(f'Please provide a valid command. Valid commands are: {valid_commands.keys()}')
