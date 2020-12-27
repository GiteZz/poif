from dataclasses import fields

from flask import jsonify, make_response, request, send_file

from poif.data.cache.disk_over_http import (GET_FILE_PATH, GET_FILES_PATH,
                                            GET_SIZE_PATH)
from poif.data.cache.disk_over_http.server import app, cache_config
from poif.data.datapoint.disk_cached import DiskCachedDataPoint
from poif.data.origin.dvc import DvcOrigin

cached_objects = {}


def get_files_from_request(request_args):
    dvc_origin = get_dataclass_from_cache(request_args, DvcOrigin)

    return dvc_origin.tag_to_original_file


def get_dataclass_from_cache(request_args, class_def):
    data_class_params = get_params_for_dataclass(request_args, class_def)
    extracted_params = {key: value for key, value in request_args if key in data_class_params}

    cache_key = tuple([extracted_params[key] for key in sorted(extracted_params.keys())])

    if cache_key not in cached_objects:
        cached_objects[cache_key] = class_def(**extracted_params)

    return cached_objects[cache_key]

def get_file_from_datapoint(request_args):
    dvc_origin = get_dataclass_from_cache(request_args, DvcOrigin)
    cache_key = dvc_origin


def get_params_for_dataclass(request, class_type):
    required_params = {field.name for field in fields(class_type) if field.init}
    url_params = set(request.args.keys())

    intersection = required_params.difference(url_params)

    return intersection


def request_to_dataclass(request, class_type):
    required_params = {field.name for field in fields(class_type) if field.init}
    url_params = set(request.args.keys())

    missing_params = get_params_for_dataclass()

    if len(missing_params) > 0:
        raise Exception(f'Missing parameters: {list(missing_params)}')

    needed_params = {key: value for key, value in request.args if key in required_params}

    return class_type(**needed_params)


@app.route(GET_FILES_PATH)
def route_get_dvc_files():
    return jsonify(get_files_from_request(request.args))


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


@app.route(GET_SIZE_PATH)
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
