"""
poif.file_system contains a toolset for working with a FUSE filesystem within the PO-IF framework. Most of the code here
should not directly be used. Instead of using this code, `poif.dataset.file_system.base.FileSystemCreator`
should be used. This class provides an interface for converting the dataset into a virtual filesystem. Only the
`poif.file_system.directory.Directory` class is used there.

"""
