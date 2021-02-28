import subprocess
from pathlib import Path

from poif.tests import get_temp_path
from poif.utils import get_relative_path
from poif.versioning.tests.utils import setup_test_package


def test_python_package():
    base_dir, git_url, original_files = setup_test_package()
    print(base_dir)

    venv_dir = get_temp_path(prefix="venv_dir") / "venv"
    python_loc = venv_dir / "bin" / "python"
    poif_setup_location = Path(__file__).parents[3]

    subprocess.run(["python3", "-m", "venv", str(venv_dir)], check=True)
    subprocess.run([str(python_loc), "-m", "pip", "install", "--upgrade", "setuptools", "pip"], check=True)
    subprocess.run([str(python_loc), "-m", "pip", "install", str(poif_setup_location)], check=True)

    subprocess.run([str(python_loc), "-m", "pip", "install", str(base_dir)], check=True)

    download_script = Path(__file__).parent / "python_package" / "download_to_folder.py"
    download_to_folder = get_temp_path(prefix="download_to_folder")
    print(download_to_folder)

    subprocess.run([str(python_loc), str(download_script), str(download_to_folder)], check=True)

    assert len(original_files) > 0
    for original_file in original_files:
        rel_path = get_relative_path(base_dir=base_dir, file=original_file)

        with open(original_file, "rb") as f:
            original_bytes = f.read()

        with open(download_to_folder / rel_path, "rb") as f:
            downloaded_bytes = f.read()

        assert original_bytes == downloaded_bytes
