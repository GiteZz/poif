import time

import requests


def is_alive(url):
    # TODO bit crude
    try:
        r = requests.get(url)
        return True
    except:
        print("Not ready")
        return False


def wait_on_url(url: str, timout=600, interval=10):
    time_started = time.time()

    while time.time() - time_started < timout:
        if is_alive(url):
            break
        else:
            print("Not ready")
        time.sleep(interval)
    # TODO crude
    time.sleep(20)  # Gitlab takes a bit longer
    print("Ready")
