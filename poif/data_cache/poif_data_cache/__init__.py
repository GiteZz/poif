from flask import Flask
app = Flask(__name__)

import poif_data_cache.server.views
# from poif_data_cache.config import mapping

# app.run(host='0.0.0.0', port=5001, debug=True)