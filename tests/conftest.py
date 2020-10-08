import os
from .settings import *


def pytest_sessionstart(session):

    # all operation should be in playground
    if not os.path.exists(PLAYGROUND_DIR):
        os.mkdir(PLAYGROUND_DIR)

    os.chdir(PLAYGROUND_DIR)

    # delete migrations dir if exists
    cleanup()
