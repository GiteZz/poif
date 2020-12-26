from poif.data.cache.disk_over_http.server import app


def run(port, host='0.0.0.0', debug=False):
    app.run(host=host, port=port, debug=False)

