import json

import dramatiq
from bson import json_util
from dramatiq.brokers.redis import RedisBroker
from flask import Flask, request, send_file
from flask_restx import Api, Resource, fields

from backend.models import Tags, Videos

app = Flask(__name__)
api = Api(app)

redis_broker = RedisBroker(host="redis")
dramatiq.set_broker(redis_broker)


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


@api.route("/api/v2/reindex-all")
class ReindexAllEndpoint(Resource):
    def post(self):
        import backend.indexing as indexing
        import backend.settings

        # set is not JSON serializable, so we have to convert to list
        directories = list(backend.settings.settings.scanned_directories)
        extensions = list(backend.settings.settings.video_extensions)

        indexing.reindex_all.send(
            directories,
            extensions,
        )
        return {"message": "success"}


@api.route("/api/v2/source-file/<id>")
class SourceFileEndpoint(Resource):
    def get(self, id):
        video = Videos.get(id)  # noqa

        file_path = ...
        file_name = ...  # noqa

        # Get the range of bytes requested by the client
        range_header = request.headers.get("Range")
        start, end = 0, None  # noqa

        if range_header:
            pass

        return send_file(
            file_path,
        )
