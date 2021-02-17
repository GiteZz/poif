from pathlib import Path


def get_template_dir():
    return Path(__file__).parent


def get_python_package_template_dir():
    return get_template_dir() / "python_package"


def get_datasets_template_dir():
    return get_template_dir() / "datasets"
