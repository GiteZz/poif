from flask import Flask
from flask import request, jsonify, send_file
# from poif_data_cache import app
from poif_data_cache.data_handling.dvc import get_dataset_info, get_file_path


app = Flask(__name__)


@app.route('/datasets/get_dvc_files')
def route_get_dvc_files():
    url_params = list(request.args.keys())
    if 'git_url' not in url_params:
        return 'git_url not in params', 422
    if 'commit' not in url_params:
        return 'commit not in params', 422
    ds_info = get_dataset_info(request.args['git_url'], request.args['commit'])
    return jsonify({'dataset_id': ds_info.id, 'files': ds_info.files})


@app.route('/datasets/get_file_content')
def route_get_file_contents():
    url_params = list(request.args.keys())
    if 'dataset_id' not in url_params:
        return 'git_url not in params', 422
    if 'file_tag' not in url_params:
        return 'commit not in params', 422
    return send_file(get_file_path(dataset_id=request.args['dataset_id'], file_id=request.args['file_tag']))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)