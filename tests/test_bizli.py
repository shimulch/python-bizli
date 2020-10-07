import os
import pytest
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


@pytest.mark.parametrize('database', ['default', 'xyz'])
def test_create_default(database):
    runner.invoke(app, ["init"])
    if database == 'default':
        result = runner.invoke(app, ["create", "test_migration"])
    else:
        result = runner.invoke(app, ["create", "test_migration", "--database", database])
    db_migration_dir = os.path.join(MIGRATION_DIR, database)
    assert result.exit_code == 0
    assert os.path.exists(db_migration_dir)
    migrations = os.listdir(db_migration_dir)
    assert len(migrations) == 1
    assert os.path.exists(os.path.join(db_migration_dir, migrations[0], 'up.sql'))
    assert os.path.exists(os.path.join(db_migration_dir, migrations[0], 'down.sql'))
    cleanup()