from dataclasses import fields

from flask import jsonify, make_response, request, send_file

from poif.data.access.datapoint import DvcDataPoint
from poif.data.access.origin import DvcOrigin
from poif.data.cache.disk_over_http import GET_FILE_PATH, GET_FILES_PATH
from poif.data.cache.disk_over_http.server import app, file_cache


def request_to_dataclass(request, class_type):
    required_params = {field.name for field in fields(class_type) if field.init}
    url_params = set(request.args.keys())

    missing_params = required_params.difference(url_params)

    if len(missing_params) > 0:
        raise Exception(f'Missing parameters: {list(missing_params)}')

    needed_params = {key: value for key, value in request.args if key in required_params}

    return class_type(**needed_params)


@app.route(GET_FILES_PATH)
def route_get_dvc_files():
    try:
        dvc_origin = request_to_dataclass(request, DvcOrigin)
    except Exception as e:
        return e, 400

    ds_info = file_cache.get_dataset_info(dvc_origin)

    return jsonify(ds_info.files)


@app.route(GET_FILE_PATH)
def route_get_file_contents():
    try:
        dvc_datapoint = request_to_dataclass(request, DvcDataPoint)
    except Exception as e:
        return e, 400

    data_file_path = file_cache.get_file_path(dvc_datapoint)
    extension = file_cache.get_extension(dvc_datapoint)

    response = make_response(send_file(data_file_path))
    response.headers['extension'] = extension
    return response


print('Views loaded')
