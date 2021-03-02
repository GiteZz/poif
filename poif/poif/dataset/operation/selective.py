from typing import Dict, List

from poif.dataset.operation.base import Operation
from poif.typing import SubSetName


class SelectiveSubsetOperation(Operation):
    def __init__(self, operations: Dict[SubSetName, "Operation"]):
        super().__init__()
        self.operations = operations

    @property
    def subsets(self) -> List[str]:
        return list(self.operations.keys())

    def __getitem__(self, subset: SubSetName) -> "Operation":
        return self.operations[subset]
