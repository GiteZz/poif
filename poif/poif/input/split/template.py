from poif.input.base import DataSetObject
from poif.input.split.base import Splitter
from poif.input.transform.tools import extract_values
from poif.typing import SubSetName


class SplitByTemplate(Splitter):
    def __init__(self, template: str, subset_tag="subset"):
        self.template = template
        self.subset_tag = subset_tag

    def split_single_input(self, ds_object: DataSetObject) -> SubSetName:
        values = extract_values(self.template, ds_object.relative_path)
        return values[self.subset_tag]
