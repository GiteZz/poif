import subprocess

def get(args):
    git_url = args[0]
    subprocess.call(['git', 'clone', git_url])
    if len(args) > 1:
        commit = args[1]
        subprocess.call(['git', 'checkout', commit])

    subprocess.call(['dvc', 'pull'])