import importlib.util
import os
import time
from collections import OrderedDict
from shutil import copyfile

import typer

from bizli.db import DatabaseProvider

app = typer.Typer()

bizli_template_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "template"
)

cwd = os.getcwd()
migration_dir = os.path.join(cwd, "migrations")
settings_file = os.path.join(migration_dir, "env.py")


def load_settings():
    """
    Load settings from migrations/settings.py

    Return:
        settings: module
    """
    spec = importlib.util.spec_from_file_location(
        "migrations.settings", settings_file
    )
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    return settings


def all_migrations(database: str):
    """
    Load all migrations for a given database
    """
    db_migration_dir = os.path.join(migration_dir, database)
    migrations = OrderedDict()
    for migration in sorted(os.listdir(db_migration_dir)):
        migrations[migration] = {
            "path": os.path.join(db_migration_dir, migration),
            "up": os.path.join(db_migration_dir, migration, "up.sql"),
            "down": os.path.join(db_migration_dir, migration, "down.sql"),
        }
    return migrations


@app.command(
    name="init",
    help="Creates a migrations directory with all required files and folders.",
)
def initialize():
    os.mkdir(migration_dir)
    files_to_copy = os.listdir(bizli_template_path)
    for file in files_to_copy:
        if os.path.isfile(file):
            copyfile(
                os.path.join(bizli_template_path, file),
                os.path.join(migration_dir, file)
            )


@app.command(name="create")
def create_migration(
    name: str,
    database: str = "default",
    settings_module: str = "migrations.settings"
):
    new_migration_folder = "{}_{}".format(
        int(time.time()), name.lower().replace(" ", "_")
    )
    db_migration_dir = os.path.join(
        migration_dir, database, new_migration_folder
    )
    up_file = os.path.join(db_migration_dir, "up.sql")
    down_file = os.path.join(db_migration_dir, "down.sql")

    if not os.path.exists(migration_dir):
        typer.echo("Bizli is not initialized. Please run `bizli init` first.")

    os.makedirs(db_migration_dir)
    open(up_file, "a").close()
    open(down_file, "a").close()


@app.command(name="migrate")
def migrate(database: str = "default", schema: str = "public"):
    settings = load_settings()

    migrations = all_migrations(database)

    db = DatabaseProvider(**settings.get_database_config(database))
    db.set_schema(schema)
    db.run_migrations(migrations)


@app.command(name="rollback")
def rollback(database: str = "default", schema: str = "public", n: int = 1):
    settings = load_settings()

    migrations = all_migrations(database)

    db = DatabaseProvider(**settings.get_database_config(database))
    db.set_schema(schema)
    db.rollback(migrations)
