import tempfile

import cv2
import numpy as np
import requests
from flask import jsonify
from httmock import HTTMock, urlmatch

from poif.data_cache.disk_over_http import GET_FILE_PATH, GET_FILES_PATH
from poif.data_cache.disk_over_http.client import RemoteCache
from poif.project_interface.classes.location import DvcDataPoint
from poif.tests import get_img


@urlmatch(path=GET_FILE_PATH)
def mock_get_file(url, request):
    img = get_img()
    img_file = tempfile.mkstemp(suffix='.png')[1]

    cv2.imwrite(img_file, img)
    return 'Feeling lucky, punk?'


datacache_url = 'datasets.com'


def test_get_file():
    remote_cache = RemoteCache(datacache_url)
    datapoint = DvcDataPoint(data_tag='aa', git_commit='aa', git_url='git.com')
    with HTTMock(mock_get_file):
        img = remote_cache.get_file(datapoint)
        assert isinstance(img, np.ndarray)