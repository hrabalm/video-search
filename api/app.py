# from pypika import Query, Table, Field
import os

import psycopg2
from flask import Flask, request

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
cur = conn.cursor()

app = Flask(__name__)


@app.get("/api/v1/get-tags")
def get_tags():
    return {"tags": ["cat", "dog", "horse", "zebra"]}


@app.post("/api/v1/search-by-tags")
def search_by_tags():
    data = request.json

    requested_tags = data['requested_tags']
    return {"message": "Success", "data": data, "requested_tags": requested_tags}


@app.get("/api/v1/show-tables")
def show_dbs():
    cur.execute("SELECT * FROM pg_catalog.pg_tables")
    x = cur.fetchall()
    return {"tables": x}
