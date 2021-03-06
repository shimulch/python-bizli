import hashlib

import psycopg2
import typer
from tqdm import tqdm

MIGRATION_TABLE_NAME = "bizli_migrations"


class DatabaseProvider:

    BIZLI_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {MIGRATION_TABLE_NAME} (
        id serial PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        hash VARCHAR(255) UNIQUE NOT NULL,
        applied_at TIMESTAMP DEFAULT NOW()
    )
    """

    def __init__(self, **kwargs):
        self.conn = psycopg2.connect(**kwargs)

    def set_schema(self, schema: str):
        self.schema = schema

    def get_schema(self):
        return self.schema if self.schema is not None else "public"

    def create_bizli_table_sql(self):
        return self.BIZLI_TABLE_SQL

    def change_schema(self):
        schema = self.get_schema()
        return f"""
            CREATE SCHEMA IF NOT EXISTS {schema};
            SET search_path TO {schema};
        """

    def insert_migration_sql(self):
        return f"""
        INSERT INTO {MIGRATION_TABLE_NAME} (name, hash) VALUES(%s, %s);
        """

    def calc_checksum(self, data):
        return hashlib.md5(data.encode("utf-8")).hexdigest()

    def get_last_migration(self):
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT name from {MIGRATION_TABLE_NAME}
                    ORDER BY applied_at DESC LIMIT 1;
                """
            )
            last_migration = None
            for row in cur.fetchall():
                last_migration = row[0]
            return last_migration

    def run_migrations(self, migrations: dict):

        with self.conn.cursor() as cur:
            cur.execute(self.change_schema())

            cur.execute(self.create_bizli_table_sql())

            last_migration = self.get_last_migration()

            migrations_to_run = list(migrations.keys())
            already_migrated = []

            if last_migration:
                index = migrations_to_run.index(last_migration)
                already_migrated = migrations_to_run[0:index + 1]
                migrations_to_run = migrations_to_run[index + 1:]

            [
                typer.echo(f"{migration} already migrated.")
                for migration in already_migrated
            ]

            if len(migrations_to_run) > 0:
                for key in migrations_to_run:
                    migration = migrations[key]
                    with open(migration["up"], "r") as f:
                        file_content = f.read()
                        cur.execute(file_content)

                        cur.execute(
                            self.insert_migration_sql(),
                            (
                                key,
                                self.calc_checksum(file_content),
                            ),
                        )
                    typer.secho(f"Applied {key}.", fg=typer.colors.GREEN)

        self.conn.commit()

    def rollback(self, migrations: dict, number = 1):

        typer.secho(f'Rolling back last {number} migrations.', fg=typer.colors.BLUE)

        with self.conn.cursor() as cur:
            cur.execute(self.change_schema())

            cur.execute(self.create_bizli_table_sql())

            while number > 0:
                last_migration = self.get_last_migration()

                if last_migration:
                    migration = migrations.get(last_migration)

                    with open(migration['down'], 'r') as f:
                        cur.execute(f.read())

                    cur.execute(f'DELETE FROM {MIGRATION_TABLE_NAME} WHERE name=%s', (last_migration,))
                    typer.secho(f'{last_migration} rolled back.', fg=typer.colors.GREEN)
                else:
                    typer.secho('Nothing to rollback!', fg=typer.colors.BLUE)
                    break

                number -= 1

        self.conn.commit()
