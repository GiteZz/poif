from torch.utils.data import DataLoader

from .dataset import pneunomia_ds
from .parameters import pneunomia_param

train_dataloader = DataLoader(pneunomia_ds.train, batch_size=pneunomia_param.batch_size)
val_dataloader = DataLoader(pneunomia_ds.val, batch_size=pneunomia_param.batch_size)