"""
`poif.tagged_data.base.TaggedData` is the basis of the entire system. The TaggedData inferface is quite simple but
still very versatile. In essence TaggedData is a piece of data with an associated tag (MD5 hash over the actual bytes).

Since the interface is so general we can use it to refer to several data repositories such data on your disk
(`poif.tagged_data.disk.DiskData`), data on S3 (`poif.tagged_data.repo.RepoData`) or even purely in memory
(`poif.tagged_data.base.StringBinaryData`).
"""
