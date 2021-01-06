from pathlib import Path


def get_python_package_template_dir():
    return Path(__file__).parent / 'package'
