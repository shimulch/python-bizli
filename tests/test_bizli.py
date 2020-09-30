from typer.testing import CliRunner

from bizli import __version__
from bizli.bizli import app

runner = CliRunner()


def test_version():
    assert __version__ == '0.1.0'


def test_app():
    result = runner.invoke(app, ["asd"])
    assert result.exit_code == 0
    assert "asd" in result.stdout
