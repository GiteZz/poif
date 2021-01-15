## Pytorch

```python
from torch import Tensor
from torch.utils.data import Dataset
from pathlib import Path
from typing import List, Tuple
import cv2

class ClassifcationDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, images: List[Path], labels: List[str]):
        self.images = images
        self.labels = labels

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> Tuple[Tensor, str]:
        img_path = self.images[idx]
        label = self.labels[idx]

        return Tensor(cv2.imread(str(img_path))), label
```

## Tensorflow / Keras (v1.x)

```python
from abc import ABC, abstractmethod
from keras_applications.resnet import ResNet50
import numpy as np
from typing import List

class PythonGenerator(ABC):
    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass

class ClassificationDataset(PythonGenerator):
    def __init__(self, images: List[np.ndarray], labels: List[str], batch_size: int = 32):
        self.images = images
        self.labels = labels
        self.batch_size = batch_size
        self.current_index = 0
        
    def __next__(self):
        img_batch = self.images[self.current_index * self.batch_size: (self.current_index + 1) * self.batch_size]
        label_batch = self.images[self.current_index * self.batch_size: (self.current_index + 1) * self.batch_size]
        current_batch = zip(img_batch, label_batch)
        
        self.current_index += 1
        return current_batch

model = ResNet50()
model.fit_generator(ClassificationDataset(dummy_images, dummy_labels))    
```

