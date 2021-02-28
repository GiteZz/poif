import sys
from pathlib import Path

from datasets.test import test

download_path = Path(sys.argv[1])

for ds_object in test.objects:
    file_on_disk = download_path / ds_object.relative_path
    file_on_disk.parent.mkdir(exist_ok=True, parents=True)
    with open(file_on_disk, "wb") as f:
        f.write(ds_object.get())
