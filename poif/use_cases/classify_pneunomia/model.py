import pytorch_lightning as pl
from torch import nn


class PneunomiaCNN(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(1, 3, 3),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(3, 12, 3),
        )