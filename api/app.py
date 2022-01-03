from flask import Flask, request
from models import Tables, Tags, Videos


app = Flask(__name__)


@app.get("/api/v1/get-tags")
def get_tags():
    return Tags.get_all()


@app.post("/api/v1/search-by-tags")
def search_by_tags():
    data = request.json

    requested_tags = data["requested_tags"]
    return {"message": "Success", "data": data, "requested_tags": requested_tags}


@app.post("/api/v1/videos")
def add_video():
    video = request.json
    Videos.add_video(video)

    return {"message": "Success"}


@app.get("/api/v1/show-tables")
def show_tables():
    return Tables.get_all()
