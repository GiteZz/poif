from flask import jsonify, make_response, request, send_file

from poif.data_cache.disk_over_http import GET_FILE_PATH, GET_FILES_PATH
from poif.data_cache.disk_over_http.server import app, file_cache
from poif.project_interface.classes.location import DvcDataPoint, DvcOrigin


@app.route(GET_FILES_PATH)
def route_get_dvc_files():
    url_params = list(request.args.keys())
    if 'git_url' not in url_params:
        return 'git_url not in params', 422
    if 'git_commit' not in url_params:
        return 'commit not in params', 422

    dvc_origin = DvcOrigin(git_url=request.args['git_url'], git_commit=request.args['git_commit'])
    ds_info = file_cache.get_dataset_info(dvc_origin)

    return jsonify(ds_info.files)


@app.route(GET_FILE_PATH)
def route_get_file_contents():
    url_params = list(request.args.keys())
    if 'git_url' not in url_params:
        return 'git_url not in params', 422
    if 'git_commit' not in url_params:
        return 'commit not in params', 422
    if 'data_tag' not in url_params:
        return 'commit not in params', 422

    dvc_datapoint = DvcDataPoint(git_url=request.args['git_url'],
                                 git_commit=request.args['git_commit'],
                                 data_tag=request.args['data_tag']
                                 )
    data_file_path = file_cache.get_file_path(dvc_datapoint)
    extension = file_cache.get_extension(dvc_datapoint)

    response = make_response(send_file(data_file_path))
    response.headers['extension'] = extension
    return response

# def response_for_file_contents


print('Views loaded')