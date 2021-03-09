"""
! Caching is still development so some problems might arise. <br>

Caching is done to avoid repeatedly downloading the same file from the remote. This is done by adding a
`poif.cache.base.CacheManager` to the DataSetObjects. The easiest way to accomplish this is by creating a CacheManager
and using the `poif.dataset.operation.transform.cache.AddCache` operation on the dataset.


A CacheManager can also be added to `poif.dataset.object.base.TransformedDataSetObject`. When added to this class the
transformed object will also be cached. This can be useful if the transformation is computational intensive or the
result is much smaller than original object (resizing etc).
"""
