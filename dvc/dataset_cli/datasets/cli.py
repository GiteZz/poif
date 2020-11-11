import argparse
import sys

from datasets.config import config
from datasets.init import init
from datasets.get import get


def main():
    args = sys.argv
    print(args)
    if len(args) <= 1:
        print(f'Please provide a command.')

    command = args[1]
    valid_commands = {
        'init': init,
        'config': config,
        'get': get
    }
    if command in valid_commands.keys():
        valid_commands[command](args[2:])
    else:
        print(f'Please provide a valid command. Valid commands are: {valid_commands.keys()}')
