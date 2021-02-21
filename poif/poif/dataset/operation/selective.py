from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from poif.dataset.operation import Operation

from poif.typing import SubSetName


class SelectiveSubsetOperation:
    def __init__(self, operations: Dict[SubSetName, "Operation"]):
        self.operations = operations

    @property
    def subsets(self) -> List[str]:
        return list(self.operations.keys())

    def __getitem__(self, subset: SubSetName) -> "Operation":
        return self.operations[subset]
