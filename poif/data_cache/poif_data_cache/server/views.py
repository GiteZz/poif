from flask import request
from poif_data_cache import app
# from poif_data_cache.config import mapping

@app.route('/datasets/get_dvc_files')
def hello():
    url_params = list(request.args.keys())
    print(url_params)
    # if 'git_url' in url_params and 'commit' in url_params:
    #     pass
    return 'Hello, World!'