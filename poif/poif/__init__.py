"""
# PO-IF

Po-if is toolset used for handling and interpreting data. 
The project can be split up into two parts, one that handles versioning and storing data on a remote. 
While the second part is aimed at creating tools that interpret that data 


## Versioning and storing data

To initialise the repository the poif package first has to be installed. This is done by cloning this repo and executing:

    pip install .
    
in the thesis/poif directory. After the package is installed the dataset can be versioned and pushed to the remote. 
This is done by going to the dataset folder and executing:

    daif init
    
This will present a cli that asks you about git information, S3 information and dataset information. 
After the prompts are finished, the data will be stored on the remote and the tracking information will be available via git.

## Tagged Data

Tagged data is the base component of the entire system. 
This is essentially a piece of data with an associated hash. 
Data is saved under their hash on the remote, this means that when the data of a file changes the remote location will change to. 
Since the data is not overwritten on the remote, the tracking information can be reverted to a previous commit and the data will still be available.
This is largely inspired by DVC. 

## Retrieving Tagged Data

### Retrieve from remote

To retrieve the tagged data from a remote we can simple use a `GitRepoCollection` that takes in the git remote url and the commit. 
On the `GitRepoCollection` we can access the TaggedData via the .get_files() operator. 
This only returns a lazy loaded reference to the data. 
This means that the actual file content will only be retrieved once the .get() operator will be called on the TaggedData.

### Retrieve from disk

If we simply want to use the interpretation framework we can also reference the data from disk. 

`tagged_data = DiskData.from_folder(ds_loc)`

The line above creates a list similar to the .get_files() operator. 
The `ds_loc` parameter is simply a pathlib.Path to the dataset location.

## Interpreting the data

In order to interpret the data we use a `Dataset`. 
This class takes in a list of `TaggedData` and converts them to `DataSetObject`. 
A `DataSetObject` is simply a `TaggedData` but with additional meta information such as annotations and label. 
Of course the data still is not changed since including it in the `Dataset`. 
To fill in this meta information we use Dataset Operations. 
All the different Operations are documented here: https://gitezz.github.io/poif/dataset/operation/index.html .

## Dataset to filesystem

Since research often works on different dataset formats, a way to transform your dataset on disk is also provided. 
This is done in the form of a `FileSystemCreator`, documented [here](https://gitezz.github.io/poif/dataset/file_system/base.html).
This class takes a dataset as input and creates a virtual filesystem and the provided location. 
Data read from the virtual filesystem will load data from the actual filesytem such that no data duplication is done.

## Examples
### Pneumonia dataset
This is how the dataset looks on disk:

```
train
  - NORMAL
    - IM-0115-0001.jpeg
    - IM-0117-0001.jpeg
    - ...
  - PNEUMONIA
    - person1_bacteria_1.jpeg
    - person1_bacteria_2.jpeg
    - ...
val
  - NORMAL
    - NORMAL2-IM-1427-0001.jpeg
    - NORMAL2-IM-1430-0001.jpeg
    - ...
  - PNEUMONIA
    - person1946_bacteria_4874.jpeg
    - person1946_bacteria_4875.jpeg
    - ...
test
  - NORMAL
    - IM-0001-0001.jpeg
    - IM-0003-0001.jpeg
    - ...
  - PNEUMONIA
    - person10_virus_35.jpeg
    - person11_virus_38.jpeg
    - ...
```

The code below is used to load the data and add the appropriate labeling / splitting.

```
from pathlib import Path
from poif.dataset.base import Dataset
from poif.dataset.object.output import classification_output
from poif.dataset.operation.split.template import SplitByTemplate
from poif.dataset.operation.transform.template import LabelByTemplate
from poif.tagged_data.disk import DiskData


ds_loc = Path("/home/user/datasets/chest_xray")
tagged_data = DiskData.from_folder(ds_loc)

template = "{{subset}}/{{label}}/*.jpeg"

add_label = LabelByTemplate(template=template)
split_into_subset = SplitByTemplate(template=template)

operations = [split_into_subset, add_label]
ds = Dataset(operations=operations, output_function=classification_output)
ds.form(tagged_data)
```

With this setup we have split the dataset into train/val/test and added a label to each object in the dataset.
Below is an example of what we have achieved.

```
ds_output = ds.train[0]  # This is the first DataSetObject in the train subset parsed by the output function
img = ds_ouput[0]        # This is the image itself as np.ndarray
label = ds_output[1]     # This is the label that corresponds to the img
```

### RPC dataset
The RPC dataset is detection dataset where on each image several product are located that have to be detected.
This is how the dataset looks on disk:

```
- instances_train2019.json
- instances_val2019.json
- instances_test2019.json
train2019
  - 0180824-13-35-55-2.jpg
  - 0180824-13-35-55-1.jpg
  - ...
val2019
  - 0180824-13-35-46-2.jpg
  - 0180824-13-35-33-2.jpg
  - ...
test2019
  - 0180824-13-35-22-2.jpg
  - 0180824-13-35-95-2.jpg
  - ...

```
The instances_*.json files are COCO annotation files. Below is the code used to transform the data to our liking.
The goal was to create a classification dataset from the detection dataset, this means that the detection crops
will be cut out and be provided with the correct label. Interpreting the COCO files happens with the
`poif.dataset.operation.transform_and_split.coco.MultiCoCo` operation. MultiCoco is a
`poif.dataset.operation.transform_and_split.base.TransformAndSplit` operation that reads the annotation files,
adds the bounding boxes to each image and the dataset in the correct subsets. In the setup below we also limit the
amount of samples to 10 for each label.
```
from poif.dataset.operation.transform.detection import DetectionToClassification
from poif.dataset.operation.transform_and_split.coco import MultiCoco
from poif.tagged_data.disk import DiskData
from poif.dataset.operation.transform.sampler import LimitSamplesByBin

ds_loc = Path("/home/gilles/datasets/retail_product_checkout")
tagged_data = DiskData.from_folder(ds_loc)

annotation_files = {
    "train": "instances_train2019.json",
    "val": "instances_val2019.json",
    "test": "instances_test2019.json",
}

data_folders = {"train": "train2019", "val": "val2019", "test": "test2019"}

coco_transform = MultiCoco(annotation_files=annotation_files, data_folders=data_folders)
limiter = LimitSamplesByBin(sample_limit=10, bin_creator=lambda x: x.label)
operations = [coco_transform, DetectionToClassification(), limiter]
ds = Dataset(operations=operations)
ds.form(tagged_data)

```
"""

__pdoc__ = {
    "poif.cli": False,
    "poif.templates": False,
    "poif.tests": False,
    "poif.packaging": False,
    "poif.typing": False,
    "poif.config": False,
    "poif.git": False
}

