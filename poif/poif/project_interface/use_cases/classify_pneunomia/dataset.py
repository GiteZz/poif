from pathlib import Path

from poif.base_classes import Dataset
from poif.data_handlers.disk_loader.gather_functions import (
    file_gatherer, poif_format_file_gatherer)

from .filters import add_pneumonia, ds_splitter, output_filter

ds_path = Path('/home/gilles/datasets/pneunomia')
file_tuples = file_gatherer(ds_path, ['.jpeg'])

pneunomia_ds = Dataset(file_tuples,
                       metadata_processors=add_pneumonia,
                       datapoint_filter=ds_splitter,
                       output_filter=output_filter
                       )