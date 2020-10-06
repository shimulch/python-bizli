import psycopg2


class DatabaseProvider:

    BIZLI_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS bizli_migrations (
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

    def get_cursor(self):
        schema = self.schema if self.schema is not None else 'public'
        cur = self.conn.cursor()
        cur.execute(f'SET search_path TO {self.schema}')
        yield cur
        cur.close()
        self.conn.commit()

    def create_bizli_table(self):
        cur = next(self.get_cursor())
        cur.execute(self.BIZLI_TABLE_SQL)

