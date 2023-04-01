import uvicorn
import httpx
import pytest
import os
import time
import contextlib
import time
import threading

from main import app


class Server(uvicorn.Server):
    '''
    Credit: https: // stackoverflow.com/a/64521239/8808175
    '''

    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


def run_sorter_server():
    config = uvicorn.Config(app,  host="0.0.0.0", port=19532,
                            timeout_keep_alive=30,  log_level="info")
    server = Server(config=config)
    return server


@pytest.fixture
def sorter_server():
    server = run_sorter_server()
    print("Uvicorn server sets up")
    with server.run_in_thread():
        yield


def test_main_sort_normal(sorter_server):
    print("Uvicorn server does set up", sorter_server)
    data = {"candidates": '{"candidates": [{"image": "https://i.ibb.co/JCj5T41/big-buck-bunny-1.png"},{"image": "https://i.ibb.co/HHJPP3R/big-buck-bunny-2.png"},{"image": "https://i.ibb.co/LPR0gb7/big-buck-bunny-3.png"},{"image": "https://i.ibb.co/qnwfks9/big-buck-bunny-4.png"},{"image": "https://i.ibb.co/56nvNHD/big-buck-bunny-5.png"},{"image": "https://i.ibb.co/jM3657F/big-buck-bunny-6.png"},{"image": "https://i.ibb.co/ZhDQshx/big-buck-bunny-7.png"},{"image": "https://i.ibb.co/0h5gD7y/big-buck-bunny-8.png"},{"image": "https://i.ibb.co/XV54Rk7/big-buck-bunny-9.png"},{"image": "https://i.ibb.co/KGwVkqy/big-buck-bunny-10.png"}, {"image": "https://i.ibb.co/J7v6p24/big-buck-bunny-11.png"}]}'}
    files = [
        ("target", ("big_buck_bunny_10.png", open(os.path.join(
            os.path.abspath('.'), "tests", "unit", "image", "big_buck_bunny_10.png"), "rb"), "image/png"))
    ]
    response = httpx.post("http://0.0.0.0:19532/sort",
                          data=data, files=files, timeout=30)
    assert response.status_code == 200
    assert response.json()[
        'result'][0]["image"] == "https://i.ibb.co/KGwVkqy/big-buck-bunny-10.png"


def test_main_sort_single(sorter_server):
    print("Uvicorn server does set up", sorter_server)
    data = {
        "candidates": '{"candidates": [{"image": "https://i.ibb.co/J7v6p24/big-buck-bunny-10.png"}]}'}
    files = [
        ("target", ("big_buck_bunny_10.png", open(os.path.join(
            os.path.abspath('.'), "tests", "unit", "image", "big_buck_bunny_10.png"), "rb"), "image/png"))
    ]
    response = httpx.post("http://0.0.0.0:19532/sort",
                          data=data, files=files, timeout=30)
    assert response.status_code == 200
    assert response.json()[
        'result'][0]["image"] == "https://i.ibb.co/KGwVkqy/big-buck-bunny-10.png"


def test_main_sort_error(sorter_server):
    print("Uvicorn server does set up", sorter_server)
    data = {
        "candidates": '{"candidates": "image": "https:/}'}
    files = [
        ("target", ("big_buck_bunny_10.png", open(os.path.join(
            os.path.abspath('.'), "tests", "unit", "image", "big_buck_bunny_10.png"), "rb"), "image/png"))
    ]
    response = httpx.post("http://0.0.0.0:19532/sort",
                          data=data, files=files, timeout=30)
    assert response.status_code == 500
