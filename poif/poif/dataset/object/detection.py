from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import Image


class DetectionInput(Image):
    def add_bounding_box(self, bbox: BoundingBox):
        self.annotations.append(bbox)

    def output(self):
        return self.get_parsed(), [annotation.output() for annotation in self.annotations]
