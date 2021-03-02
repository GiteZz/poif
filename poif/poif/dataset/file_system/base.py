import time
from abc import ABC, abstractmethod
from multiprocessing import Process
from pathlib import Path
from typing import List

from fuse import FUSE

from poif.dataset.base import Dataset
from poif.file_system.base import DataSetFileSystem
from poif.file_system.directory import Directory


class FileSystemCreator(ABC):
    """
    The FileSystemCreator class is meant to transform a dataset into an actual filesystem. This could be useful
    to test new algorithms without actually copying and transforming your original dataset.
    """

    def __call__(self, dataset: Dataset, base_dir: Path, daemon=True):
        root_dir = self.create(dataset, base_dir)
        setup_as_filesystem(root_dir, base_dir, daemon)

    @abstractmethod
    def create(self, dataset: Dataset, base_dir: Path) -> Directory:
        pass

    def get_classes_sorted_by_id(self, dataset: Dataset) -> List[str]:
        ids = list(dataset.meta.index_to_label.keys())
        assert max(ids) == len(ids) - 1

        sorted_ids = [""] * len(ids)

        for category_id, category_name in dataset.meta.index_to_label.items():
            sorted_ids[category_id] = category_name

        return sorted_ids


def setup_as_filesystem(root_dir: Directory, base_dir: Path, daemon=False):
    file_system = DataSetFileSystem(root_dir)

    p = Process(target=setup_filesystem, args=(file_system, base_dir), daemon=daemon)
    p.start()

    start_waiting = time.time()
    while not (base_dir / "__test_file").exists():
        if time.time() - start_waiting > 30:
            p.terminate()
            raise Exception("FUSE filesystem did not start correctly")
        time.sleep(0.02)

    return p


def setup_filesystem(file_system: DataSetFileSystem, system_path: Path):
    fuse_handler = FUSE(  # noqa
        file_system,
        str(system_path),
        foreground=False,
        allow_other=False,
    )
