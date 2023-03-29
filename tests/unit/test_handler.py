import uvicorn
import httpx
import pytest
from multiprocessing import Process
import os
import time

from main import app


def run_server():
    uvicorn.run(app, port=19532)


@pytest.fixture
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start()
    time.sleep(5)
    yield
    proc.kill()  # Cleanup after test


def test_main_sort():
    data = {"candidates": '{"candidates": [{"image": "https://i.ibb.co/JCj5T41/big-buck-bunny-1.png"},{"image": "https://i.ibb.co/HHJPP3R/big-buck-bunny-2.png"},{"image": "https://i.ibb.co/LPR0gb7/big-buck-bunny-3.png"},{"image": "https://i.ibb.co/qnwfks9/big-buck-bunny-4.png"},{"image": "https://i.ibb.co/56nvNHD/big-buck-bunny-5.png"},{"image": "https://i.ibb.co/jM3657F/big-buck-bunny-6.png"},{"image": "https://i.ibb.co/ZhDQshx/big-buck-bunny-7.png"},{"image": "https://i.ibb.co/0h5gD7y/big-buck-bunny-8.png"},{"image": "https://i.ibb.co/XV54Rk7/big-buck-bunny-9.png"},{"image": "https://i.ibb.co/KGwVkqy/big-buck-bunny-10.png"}, {"image": "https://i.ibb.co/J7v6p24/big-buck-bunny-11.png"}]}'}
    files = [
        ("target", ("big_buck_bunny_10.png", open(os.path.join(
            os.path.abspath('.'), "tests", "unit", "image", "big_buck_bunny_10.png"), "rb"), "image/png"))
    ]
    response = httpx.post("http://localhost:19532/sort",
                          data=data, files=files)
    assert response.status_code == 200
    assert response.json() == {
        "result": [
            {
                "image": "https://i.ibb.co/KGwVkqy/big-buck-bunny-10.png"
            },
            {
                "image": "https://i.ibb.co/qnwfks9/big-buck-bunny-4.png"
            },
            {
                "image": "https://i.ibb.co/HHJPP3R/big-buck-bunny-2.png"
            },
            {
                "image": "https://i.ibb.co/XV54Rk7/big-buck-bunny-9.png"
            },
            {
                "image": "https://i.ibb.co/ZhDQshx/big-buck-bunny-7.png"
            },
            {
                "image": "https://i.ibb.co/0h5gD7y/big-buck-bunny-8.png"
            },
            {
                "image": "https://i.ibb.co/LPR0gb7/big-buck-bunny-3.png"
            },
            {
                "image": "https://i.ibb.co/J7v6p24/big-buck-bunny-11.png"
            },
            {
                "image": "https://i.ibb.co/56nvNHD/big-buck-bunny-5.png"
            },
            {
                "image": "https://i.ibb.co/jM3657F/big-buck-bunny-6.png"
            },
            {
                "image": "https://i.ibb.co/JCj5T41/big-buck-bunny-1.png"
            }
        ]
    }
