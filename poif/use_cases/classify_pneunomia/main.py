from torch.utils.data import DataLoader

from .parameters import pneunomia_param
from .dataset import pneunomia_ds


train_dataloader = DataLoader(pneunomia_ds.train, batch_size=pneunomia_param.batch_size)
val_dataloader = DataLoader(pneunomia_ds.val, batch_size=pneunomia_param.batch_size)