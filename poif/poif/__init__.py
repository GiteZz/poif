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

