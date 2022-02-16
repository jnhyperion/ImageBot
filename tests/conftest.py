import os
import cv2
import shutil
import pytest


@pytest.fixture(scope="module")
def tests_dir():
    yield os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="module")
def tests_out_dir(tests_dir):
    out = os.path.join(tests_dir, "__out__")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    yield out


@pytest.fixture
def images(request, tests_dir):
    return (
        cv2.imread(
            os.path.join(tests_dir, f"images/{request.param}.png"), cv2.IMREAD_UNCHANGED
        ),
        cv2.imread(
            os.path.join(tests_dir, f"images/{request.param}_template.png"),
            cv2.IMREAD_UNCHANGED,
        ),
        request.param,
    )
