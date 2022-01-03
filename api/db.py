import os

import psycopg2
import psycopg2.extras
import pypika.queries
from pypika import Field, Query, Table

DB_HOST = os.getenv("SQL_HOST")
DB_PORT = os.getenv("SQL_PORT")
DB_NAME = os.getenv("SQL_DB")
DB_USER = os.getenv("SQL_USER")
DB_PASSWORD = os.getenv("SQL_PASSWORD")

print(f"{DB_HOST=}")
print(f"{DB_USER=}")
print(f"{DB_PASSWORD=}")

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
)
cursor = conn.cursor()
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def create_tables():
    q = """
        DROP TABLE IF EXISTS videos CASCADE;
        DROP TABLE IF EXISTS tags CASCADE;
        DROP TABLE IF EXISTS videos_tags CASCADE;

        CREATE TABLE IF NOT EXISTS videos (
            id serial PRIMARY KEY,
            filename text,
            md5 text,
            created timestamp,
            metadata json
        );

        CREATE TABLE IF NOT EXISTS tags (
            id serial PRIMARY KEY,
            tag text,
            tag_type text  -- redundant
        );

        CREATE TABLE IF NOT EXISTS video_tags (
            video_id int references videos(id),
            tag_id int references tags(id)
        );

        INSERT INTO tags (tag, tag_type) VALUES
            ('cat', 'nn'),
            ('dog', 'nn');
    """
    cursor.execute(q)
    conn.commit()
create_tables()
