import os
from .settings import *
from typer.testing import CliRunner

from bizli import __version__
from bizli.bizli import app

runner = CliRunner()


def test_version():
    assert __version__ == '0.1.0'


def test_init():
    """
    Test if init command creates directory correctly
    """
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert os.path.exists(MIGRATION_DIR)
    cleanup()
