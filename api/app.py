from flask import Flask, request
from models import Tables, Tags


app = Flask(__name__)


@app.get("/api/v1/get-tags")
def get_tags():
    return Tags.get_all()


@app.post("/api/v1/search-by-tags")
def search_by_tags():
    data = request.json

    requested_tags = data["requested_tags"]
    return {"message": "Success", "data": data, "requested_tags": requested_tags}


@app.get("/api/v1/show-tables")
def show_dbs():
    return Tables.get_all()
