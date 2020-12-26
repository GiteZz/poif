import collections
import logging
import os
import re
import traceback
from errno import ENOENT

import diskcache as dc
import numpy as np
import requests
from fuse import FUSE, FuseOSError, LoggingMixIn, Operations
from tenacity import retry, wait_exponential

from poif.data.file_system.utils import create_dir_attr, create_file_attr

CLEANUP_INTERVAL = 60
CLEANUP_EXPIRED = 60

REPORT_INTERVAL = 60

DISK_CACHE_SIZE_ENV = "HTTPFS_DISK_CACHE_SIZE"
DISK_CACHE_DIR_ENV = "HTTPFS_DISK_CACHE_DIR"


FALSY = {0, "0", False, "false", "False", "FALSE", "off", "OFF"}


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def __getitem__(self, key):
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def __setitem__(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value

    def __contains__(self, key):
        return key in self.cache

    def __len__(self):
        return len(self.cache)


class HttpFetcher:
    SSL_VERIFY = os.environ.get("SSL_VERIFY", True) not in FALSY

    def __init__(self, logger):
        self.logger = logger
        if not self.SSL_VERIFY:
            logger.warning(
                "You have set ssl certificates to not be verified. "
                "This may leave you vulnerable. "
                "http://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification"
            )

    def get_size(self, url):
        # If .head doesn't work try the normal GET requests
        try:
            # requests.head only requests the header instead of the entire get
            head = requests.head(url, allow_redirects=True, verify=self.SSL_VERIFY)
            return int(head.headers["Content-Length"])
        except:
            head = requests.get(
                url,
                allow_redirects=True,
                verify=self.SSL_VERIFY,
                headers={"Range": "bytes=0-1"},
            )
            crange = head.headers["Content-Range"]
            match = re.search(r"/(\d+)$", crange)
            if match:
                return int(match.group(1))

            self.logger.error(traceback.format_exc())
            raise FuseOSError(ENOENT)

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_data(self, url, start, end):
        headers = {"Range": "bytes={}-{}".format(start, end), "Accept-Encoding": ""}
        self.logger.info("gettings %s %s %s", url, start, end)
        r = requests.get(url, headers=headers)
        self.logger.info("got %s", r.status_code)
        print("got", r.status_code)
        r.raise_for_status()
        block_data = np.frombuffer(r.content, dtype=np.uint8)
        return block_data


class HttpFileSystem(LoggingMixIn, Operations):
    """
    A read only http/https/ftp filesystem.
    """

    def __init__(
        self,
        disk_cache_size=2 ** 30,
        disk_cache_dir="/tmp/xx",
        lru_capacity=400,
        block_size=2 ** 20,
        logger=None,
    ):
        self.lru_cache = LRUCache(capacity=lru_capacity)
        self.lru_attrs = LRUCache(capacity=lru_capacity)
        self.schema = 'http'
        self.logger = logger
        self.last_report_time = 0
        self.total_requests = 0
        self.getting = set()

        if not self.logger:
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(logging.FileHandler('/tmp/fuse_logs.txt'))
            self.logger.setLevel(logging.DEBUG)

        self.logger.info("Starting with disk_cache_size: %d", disk_cache_size)

        self.fetcher = HttpFetcher(self.logger)

        self.disk_cache = dc.Cache(disk_cache_dir, size_limit=disk_cache_size)

        self.total_blocks = 0
        self.lru_hits = 0
        self.lru_misses = 0

        self.disk_hits = 0
        self.disk_misses = 0
        self.block_size = block_size

        f = open("/home/gilles/datasets/pneumonia/test/NORMAL/IM-0001-0001.jpeg", "rb")
        num = bytearray(f.read())

        self.file = num

    def getSize(self, url):
        print('getSize')
        try:
            return self.fetcher.get_size(url)
        except Exception as ex:
            self.logger.exception(ex)
            raise

    def readdir(self, path, fh):
        print('readdir')
        return ['.', '..'] + ['Hello']

    def getattr(self, path, fh=None):
        print(f'getattr on path {path}')
        try:
            if path == "/":
                self.lru_attrs[path] = create_dir_attr(0o555)
                return self.lru_attrs[path]

            if path == '/Hello':
                return create_file_attr(0o644, size=len(self.file))

            # size = self.getSize(url)
            # print(f'size: {size}')
            size = 5
            # logging.info("head: {}".format(head.headers))
            # logging.info("status_code: {}".format(head.status_code))
            # print("url:", url, "head.url", head.url)

            if size is not None:
                return create_file_attr(0o644, size=size)
            else:
                return create_dir_attr(0o555)

        except Exception as ex:
            self.logger.exception(ex)
            raise

    def unlink(self, path):
        return 0

    def create(self, path, mode, fi=None):
        return 0

    def write(self, path, buf, size, offset, fip):
        return 0

    def read(self, path, size, offset, fh):
        print(f'read on path: {path}, size: {size}, offset: {offset}, fh: {fh}')

        if 'autorun.inf' in path:
            return
        if '.' == path[1]:
            return
        if path == '/Hello':
            return bytes(self.file[offset: offset + size])
        # try:
        #     # self.total_requests += 1
        #     # if path in self.lru_attrs:
        #     #     url = "{}:/{}".format(self.schema, path[:-2])
        #     #
        #     #     self.logger.debug("read url: {}".format(url))
        #     #     self.logger.debug(
        #     #         "offset: {} - {} request_size (KB): {:.2f} block: {}".format(
        #     #             offset,
        #     #             offset + size - 1,
        #     #             size / 2 ** 10,
        #     #             offset // self.block_size,
        #     #         )
        #     #     )
        #     #     output = np.zeros((size,), np.uint8)
        #     #
        #     #     t1 = time()
        #     #
        #     #     # nothing fetched yet
        #     #     last_fetched = -1
        #     #     curr_start = offset
        #     #
        #     #     while last_fetched < offset + size:
        #     #         block_num = curr_start // self.block_size
        #     #         block_start = self.block_size * (curr_start // self.block_size)
        #     #
        #     #         block_id = (url, block_num)
        #     #         while block_id in self.getting:
        #     #             sleep(0.05)
        #     #
        #     #         self.getting.add(block_id)
        #     #         block_data = self.get_block(url, block_num)
        #     #         self.getting.remove(block_id)
        #     #
        #     #         data_start = (
        #     #             curr_start - (curr_start // self.block_size) * self.block_size
        #     #         )
        #     #
        #     #         data_end = min(self.block_size, offset + size - block_start)
        #     #         data = block_data[data_start:data_end]
        #     #
        #     #         d_start = curr_start - offset
        #     #         output[d_start : d_start + len(data)] = data
        #     #
        #     #         last_fetched = curr_start + (data_end - data_start)
        #     #         curr_start += data_end - data_start
        #     #
        #     #     bts = bytes(output)
        #     #
        #     #     return bts
        #         return self.file[offset: offset + size]
        #
        #     # else:
        #     #     logging.info("file not found: {}".format(path))
        #     #     raise FuseOSError(EIO)
        # except Exception as ex:
        #     self.logger.exception(ex)
        #     raise

    def destroy(self, path):
        self.disk_cache.close()

    def get_block(self, url, block_num):
        """
        Get a data block from a URL. Blocks are 256K bytes in size
        Parameters:
        -----------
        url: string
            The url of the file we want to retrieve a block from
        block_num: int
            The # of the 256K'th block of this file
        """
        cache_key = "{}.{}.{}".format(url, self.block_size, block_num)
        cache = self.disk_cache

        self.total_blocks += 1

        if cache_key in self.lru_cache:
            self.lru_hits += 1
            hit = self.lru_cache[cache_key]
            return hit
        else:
            self.lru_misses += 1

            if cache_key in self.disk_cache:
                self.logger.info("cache hit: %s", cache_key)
                try:
                    block_data = self.disk_cache[cache_key]
                    self.disk_hits += 1
                    self.lru_cache[cache_key] = block_data
                    return block_data
                except KeyError:
                    pass

            self.disk_misses += 1
            block_start = block_num * self.block_size

            self.logger.info("getting data %s", cache_key)
            block_data = self.fetcher.get_data(
                url, block_start, block_start + self.block_size - 1
            )

            self.lru_cache[cache_key] = block_data
            self.disk_cache[cache_key] = block_data

        return block_data

if __name__ == "__main__":
    fuse = FUSE(
        HttpFileSystem(
               disk_cache_size=2**30,
               disk_cache_dir='/tmp/xx',
               lru_capacity=400,
               block_size=2**20,
            ),
        '/home/gilles/fuse_test',
        foreground=True,
        allow_other=False
    )