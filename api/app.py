from flask import Flask, request
from models import Tags, Videos


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
    Videos.add(video)

    return {"message": "Success"}


@app.get("/api/v1/videos")
def get_all_videos():
    return Videos.get_all()
