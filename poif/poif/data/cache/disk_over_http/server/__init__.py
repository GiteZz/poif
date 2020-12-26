from pathlib import Path

from flask import Flask

app = Flask(__name__)

from poif.data.cache.disk import LocalCache

file_cache = LocalCache(work_dir=Path.cwd() / 'file_cache')

from poif.data.cache.disk_over_http.server import views
