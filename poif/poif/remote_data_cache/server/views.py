from flask import request, jsonify, send_file
from poif.project_interface.classes.location import DvcDataPoint, DvcOrigin

from poif.remote_data_cache.server import app, file_cache


@app.route('/datasets/files')
def route_get_dvc_files():
    url_params = list(request.args.keys())
    if 'git_url' not in url_params:
        return 'git_url not in params', 422
    if 'git_commit' not in url_params:
        return 'commit not in params', 422

    dvc_origin = DvcOrigin(git_url=request.args['git_url'], git_commit=request.args['git_commit'])
    ds_info = file_cache.get_dataset_info(dvc_origin)

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

    dvc_datapoint = DvcDataPoint(git_url=request.args['git_url'], git_commit=request.args['git_commit'], data_tag=request.args['file_tag'])
    file_path = file_cache.get_file_path(dvc_datapoint)

    return send_file(file_path)


print('Views loaded')