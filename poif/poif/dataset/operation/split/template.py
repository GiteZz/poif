from typing import Optional

from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.split.base import Splitter
from poif.typing import SubSetName
from poif.utils.template import extract_values


class SplitByTemplate(Splitter):
    def __init__(self, template: str, subset_tag="subset"):
        self.template = template
        self.subset_tag = subset_tag

    def split_single_input(self, ds_object: DataSetObject) -> Optional[SubSetName]:
        values = extract_values(self.template, ds_object.relative_path)

        if self.subset_tag in values:
            return values[self.subset_tag]
        else:
            return None
