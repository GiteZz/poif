from poif.project_interface.classes.resource import DataFilePath, Image
import cv2


def load(path: DataFilePath):
    extension = path.parts[-1].split('.')[-1]
    if extension in ['jpg', 'png', 'jpeg']:
        return img_loader(path)
    else:
        raise NotImplementedError()


def img_loader(path: DataFilePath) -> Image:
    img = cv2.imread(str(path))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)