import os
import shutil

PLAYGROUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'playground')
MIGRATION_DIR = os.path.join(PLAYGROUND_DIR, 'migrations')


def cleanup():
    if os.path.exists(MIGRATION_DIR):
        shutil.rmtree(MIGRATION_DIR)

