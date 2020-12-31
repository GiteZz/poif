import subprocess
from pathlib import Path

from poif.utils.git import GitRepo


def push(args):
    git_repo = GitRepo(Path.cwd())
    subprocess.call(['dvc', 'push'])
    subprocess.call(['git', 'push', '-u', 'origin', 'master'])