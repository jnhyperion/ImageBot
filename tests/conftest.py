import os
import shutil
import pytest


@pytest.fixture(scope="module")
def tests_dir():
    yield os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="module")
def tests_out_dir(tests_dir, worker_id):
    out = os.path.join(tests_dir, "__out__", worker_id)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    yield out


@pytest.fixture
def images(request, tests_dir):
    return (
        os.path.join(tests_dir, f"images/{request.param}.png"),
        os.path.join(tests_dir, f"images/{request.param}_template.png"),
        request.param,
    )
