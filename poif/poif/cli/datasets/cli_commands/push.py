import subprocess


def push(args):
    subprocess.call(['dvc', 'push'])
    subprocess.call(['git', 'push', '-u', 'origin', 'master'])