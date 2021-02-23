from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from poif.dataset.base import MultiDataset


class FileSystemCreator(ABC):
    @abstractmethod
    def create(self, dataset: MultiDataset, base_dir: Path, daemon=True):
        pass

    def get_classes_sorted_by_id(self, dataset: MultiDataset) -> List[str]:
        ids = list(dataset.meta.index_to_label.keys())
        assert max(ids) == len(ids) - 1

        sorted_ids = [""] * len(ids)

        for category_id, category_name in dataset.meta.index_to_label.items():
            sorted_ids[category_id] = category_name

        return sorted_ids
