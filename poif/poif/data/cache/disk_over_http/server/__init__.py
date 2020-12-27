from pathlib import Path

from flask import Flask

app = Flask(__name__)

from poif.data.cache.disk import CacheConfig

default_work_dir = Path('./datasets_cache')

cache_config = CacheConfig(default_work_dir)

from poif.data.cache.disk_over_http.server import views
