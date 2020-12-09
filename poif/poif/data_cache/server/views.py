from flask import request, jsonify, send_file
from poif.data_cache.data_handling.dvc import get_dataset_info, get_file_path

from poif.data_cache.server import app



@app.route('/datasets/files')
def route_get_dvc_files():
    url_params = list(request.args.keys())
    if 'git_url' not in url_params:
        return 'git_url not in params', 422
    if 'git_commit' not in url_params:
        return 'commit not in params', 422
    ds_info = get_dataset_info(request.args['git_url'], request.args['git_commit'])
    return jsonify(ds_info.files)


@app.route('/datasets/file_content')
def route_get_file_contents():
    url_params = list(request.args.keys())
    if 'git_url' not in url_params:
        return 'git_url not in params', 422
    if 'git_commit' not in url_params:
        return 'commit not in params', 422
    if 'file_tag' not in url_params:
        return 'commit not in params', 422
    return send_file(get_file_path(request.args['git_url'], request.args['git_commit'], file_id=request.args['file_tag']))


print('Views loaded')