from pathlib import Path

from flask import Flask

app = Flask(__name__)

from poif.cache.disk import CacheConfig

default_work_dir = Path("./datasets_cache")

cache_config = CacheConfig(default_work_dir)
