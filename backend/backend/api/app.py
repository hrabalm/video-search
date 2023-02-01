import json

from bson import json_util
from flask import Flask
from flask_restx import Api, Resource, fields

from backend.models import Tags, Videos

app = Flask(__name__)
api = Api(app)


def jsonify(x):
    return json.loads(json_util.dumps(x))


@api.route("/api/v2/tags")
class TagsEndpoint(Resource):
    def get(self):
        return {"tags": Tags.get_all()}


@api.route("/api/v2/videos")
class VideosEndpoint(Resource):
    def get(self):
        return {"videos": jsonify(Videos.get_all())}


@api.route("/api/v2/videos/<id>")
class VideoEndpoint(Resource):
    def get(self, id):
        return {"video": jsonify(Videos.get(id))}


videos_by_tags_post_req = api.model(
    "QueryVideosByTagRequest",
    {
        "tags": fields.List(fields.String),
    },
)


@api.route("/api/v2/videos-by-tags")
class VideosByTagEndpoint(Resource):
    def get(self, tags):
        return {"videos": jsonify(Videos.get_by_tags(tags, 0.5))}

    @api.expect(videos_by_tags_post_req)
    def post(self):
        if api.payload and "tags" in api.payload:
            tags = api.payload["tags"]
            videos_found = jsonify(Videos.get_by_tags(tags, 0.0))
            return {
                "videos": videos_found,
            }
        else:
            return {}
