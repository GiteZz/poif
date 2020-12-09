from flask import Flask
app = Flask(__name__)

from poif.data_cache.server import views

