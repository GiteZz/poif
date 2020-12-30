from pathlib import Path


def cleanup(args):
    possible_files = ['README.md', 'setup.py']
    for file in possible_files:
        file_path = Path.cwd() / file
        if file_path.exists():
            file_path.unlink()

    possible_directories = ['datasets', '.cache']
    for directory in possible_directories:
        directory_path = Path.cwd() / directory
        if directory_path.exists():
            delete_folder(directory_path)

def delete_folder(pth) :
    for sub in pth.iterdir() :
        if sub.is_dir() :
            delete_folder(sub)
        else :
            sub.unlink()
    pth.rmdir()