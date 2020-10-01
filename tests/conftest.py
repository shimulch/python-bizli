import os
from .settings import *


def pytest_sessionstart(session):

    # all operation should be in playground
    os.chdir(PLAYGROUND_DIR)

    # delete migrations dir if exists
    cleanup()
