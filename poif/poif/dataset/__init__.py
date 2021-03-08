"""
# `poif.dataset.base.Dataset`
`poif.dataset.base.Dataset` implements the standard pytorch dataset interface combined with some nice extras.
Notably the option to perform dataset operations.


## `poif.dataset.operation.base.Operation`

An operation on a dataset is meant to change the dataset and/or its contents.
An operation can be applied via the .apply_operation() method on an existing dataset.
A list of operation can also be given in the constructor which will then be used over the inputs
when the dataset is constructed via the form() method.

### `poif.dataset.operation.split.base.Splitter`

A Splitter operation is meant for creating subdatasets within the dataset.
These subdatasets (also instance of `poif.dataset.base.Dataset`) are meanly meant for creating the
train/val/test split, but can of course be used to your liking.
The subdatasets can simply be accessed with the '.' on the dataset variable.

```
birds_ds = Dataset()

train_val_splitter = Splitter()

bird_ds.apply_operation(train_val_splitter)



bird_ds.train -> Contains training data

bird_ds.val -> Contains validation data
```

### `poif.dataset.operation.transform.base.Transformation`

The Transformation is meant to change the internal DataSet objects. An example of this could be
adding the labels from the original path (`poif.dataset.operation.transform.template.LabelByTemplate`).
Another example is removing specific samples (`poif.dataset.operation.transform.template.DropByTemplate`).
or limiting the amount of samples per bin (`poif.dataset.operation.transform.sampler.LimitSamplesByBin`).

### `poif.dataset.operation.meta_provider.base.MetaProvider`

The MetaProvider is meant to add or transform the metadata of the dataset. The metadata is
accessible via the .meta on the dataset and will return a MetaCollection dataset.

### `poif.dataset.operation.transform_and_split.base.TransformAndSplit`

The TransformAndSplit combines the Splitter and Transformation. This is useful with datasets where
the split and additional data is located in one metafile.

### `poif.dataset.operation.selective.SelectiveSubsetOperation`

The last operation is the SelectiveSubsetOperation, this operation simply allows for using operation on a
selective subset. This could be used to limit the samples in train and validation by a different amount.
"""