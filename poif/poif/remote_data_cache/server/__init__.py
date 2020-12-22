from flask import Flask
from pathlib import Path
app = Flask(__name__)

from poif.local_data_cache import LocalCache

file_cache = LocalCache(work_dir=Path.cwd() / 'file_cache')

from poif.remote_data_cache.server import views

