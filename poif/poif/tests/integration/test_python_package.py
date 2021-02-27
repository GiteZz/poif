import subprocess

from poif.tests import get_temp_path
from poif.tests.repo import create_realistic_folder_structure


def test_python_package():
    base_dir, folder, files = create_realistic_folder_structure()
    venv_dir = get_temp_path()

    subprocess.call(["python3", "-m", "venv", str(venv_dir)])
