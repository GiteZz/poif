import json
import tempfile

import cv2
from httmock import HTTMock, all_requests, response

from poif.data.access.datapoint import DvcDataPoint
from poif.data.access.origin import DvcOrigin
from poif.data.cache.disk_over_http.client import RemoteCache
from poif.tests import get_img

img = get_img()

img_extension = 'png'
img_file = tempfile.mkstemp(suffix=f'.{img_extension}')[1]
cv2.imwrite(img_file, img)


@all_requests
def mock_get_file(url, request):

    with open(img_file, 'rb') as f:
        img_bytes = f.read()

    headers = {'extension': img_extension}
    content = img_bytes
    return response(200, content, headers)

test_files = {
        'aa': '01.jpg',
        'bb': '02.jpg'
    }

@all_requests
def mock_get_files(url, request):
    headers = {'mimetype':' application/json'}

    return response(200, json.dumps(test_files), headers)


datacache_url = 'http://datasets.com'


def test_get_file():
    remote_cache = RemoteCache(datacache_url)
    datapoint = DvcOrigin(git_commit='aa', git_url='git.com')
    with HTTMock(mock_get_file):
        # This is read in RGB
        cache_img = remote_cache.get_files(datapoint)

        # This is read in BGR
        original_img = cv2.imread(img_file)
        original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

        assert (cache_img == original_img_rgb).all()


def test_get_files():
    remote_cache = RemoteCache(datacache_url)
    origin = DvcDataPoint(data_tag='aa', git_commit='aa', git_url='git.com')
    with HTTMock(mock_get_files):
        # This is read in RGB
        retrieved_files = remote_cache.get_files(origin)

        assert retrieved_files == test_files