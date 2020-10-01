import typer
import os
from shutil import copyfile

app = typer.Typer()

bizli_template_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'template'
)


@app.command(name='init', help="Creates a migrations directory with all required files and folders.")
def initialize():
    cwd = os.getcwd()
    migration_dir = os.path.join(cwd, 'migrations')
    os.mkdir(migration_dir)
    files_to_copy = os.listdir(bizli_template_path)
    for file in files_to_copy:
        copyfile(os.path.join(bizli_template_path, file), os.path.join(migration_dir, file))


@app.command(name='new')
def create_migration(name: str):
    pass
