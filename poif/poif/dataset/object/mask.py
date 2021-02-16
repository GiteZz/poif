from poif.dataset.object.annotations import Mask
from poif.dataset.object.base import DataSetObject


class SingleMaskObject(DataSetObject):
    def output(self):
        assert len(self.annotations) == 1
        assert isinstance(self.annotations[0], Mask)

        return self.get_parsed(), self.annotations[0].output()
