from flask import request, jsonify
from poif_data_cache import app
from poif_data_cache.data_handling.dvc import get_dvc_files
from poif_data_cache.config import mapping


@app.route('/datasets/get_dvc_files')
def hello():
    url_params = list(request.args.keys())
    if 'git_url' not in url_params:
        return 'git_url not in params', 422
    if 'commit' not in url_params:
        return 'commit not in params', 422
    return jsonify(get_dvc_files(request.args['git_url'], request.args['commit']))


@app.route('/datasets/get_file_content')
def hello():
    url_params = list(request.args.keys())
    if 'git_url' not in url_params:
        return 'git_url not in params', 422
    if 'commit' not in url_params:
        return 'commit not in params', 422
    return jsonify(get_dvc_files(request.args['git_url'], request.args['commit']))