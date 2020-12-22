from poif.remote_data_cache.server import app


def run(port, host='0.0.0.0', debug=False):
    app.run(host=host, port=port, debug=False)

