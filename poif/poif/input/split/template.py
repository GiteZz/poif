from poif.input.split.base import Splitter
from poif.input.tagged_data import TaggedDataInput
from poif.input.transform.tools import extract_values
from poif.typing import SubSetName


class SplitByTemplate(Splitter):
    def __init__(self, template: str, subset_tag="subset"):
        self.template = template
        self.subset_tag = subset_tag

    def split_single_input(self, ds_input: TaggedDataInput) -> SubSetName:
        values = extract_values(self.template, ds_input.relative_path)
        return values[self.subset_tag]
