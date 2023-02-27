import json
import pathlib

import werkzeug.exceptions
from bson import json_util
from flask import Flask, send_file
from flask_restx import Api, Resource, fields

import backend.settings
import backend.tasks
import backend.tasks.default
from backend.models import Tags, Videos

app = Flask(__name__)
api = Api(app)


def jsonify(x):
    return json.loads(json_util.dumps(x))


@api.route("/api/heartbeat")
class Heartbeat(Resource):
    def get(self):
        return {"status": "healthy"}


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


@api.route("/api/v2/index-new-files")
class IndexNewFilesEndpoint(Resource):
    def post(self):
        # set is not JSON serializable, so we have to convert to list
        directories = list(backend.settings.settings.scanned_directories)
        extensions = list(backend.settings.settings.video_extensions)

        backend.tasks.default.rpc_index_new_files.send(
            directories,
            extensions,
        )
        return {"message": "success"}


@api.route("/api/v2/reindex-all")
class ReindexAllEndpoint(Resource):
    def post(self):
        # set is not JSON serializable, so we have to convert to list
        directories = list(backend.settings.settings.scanned_directories)
        extensions = list(backend.settings.settings.video_extensions)

        backend.tasks.default.rpc_reindex_all.send(
            directories,
            extensions,
        )
        return {"message": "success"}


@api.route("/api/v2/source-file/<id>")
class SourceFileEndpoint(Resource):
    def get(self, id):
        video = Videos.get(id)

        if not video:
            raise werkzeug.exceptions.NotFound(f"Object with id '{id}' not found.")

        file_path = pathlib.Path(video["filenames"][0])
        file_name = file_path.name
        file_extension = file_path.suffix

        # TODO: these definitions could be moves elsewhere (and potentially
        # be joined with a list of supported multimedia formats)
        MIMETYPES = {
            ".mp4": "video/mp4",
            ".mkv": "video/x-matroska",
            ".flv": "video/x-flv",
            ".webm": "video/webm",
            ".avi": "video/x-msvideo",
            ".wmv": "video/x-ms-wmv",
        }
        DEFAULT_VIDEO_MIMETYPE = "application/octet-stream"
        file_mimetype = MIMETYPES.get(file_extension, DEFAULT_VIDEO_MIMETYPE)

        return send_file(
            file_path,
            download_name=file_name,
            mimetype=file_mimetype,
        )
