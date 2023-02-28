import json
import pathlib

import werkzeug.exceptions
from bson import json_util
from flask import Flask, Response, send_file
from flask_restx import Api, Resource, fields

import backend.tasks
import backend.tasks.default
from backend.models import Tags, Videos
from backend.settings import settings

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
        "count_per_page": fields.Integer(default=100),
        "last_filename": fields.String(default=""),
    },
)


@api.route("/api/v2/videos-by-tags")
class VideosByTagEndpoint(Resource):
    def get(self, tags, items_per_page, page_number):
        return {
            "videos": jsonify(
                Videos.get_by_tags_with_pagination(
                    tags,
                    settings.minimum_confidence_shown,
                    items_per_page,
                    page_number,
                )
            )
        }

    @api.expect(videos_by_tags_post_req)
    def post(self):
        if api.payload and "tags" in api.payload:
            tags = api.payload["tags"]
            items_per_page = api.payload["items_per_page"]
            page_number = api.payload["page_number"]
            print(tags, items_per_page, page_number, flush=True)
            videos_found = jsonify(
                Videos.get_by_tags_with_pagination(
                    tags,
                    settings.minimum_confidence_shown,
                    items_per_page,
                    page_number,
                )
            )
            return {
                "videos": videos_found,
            }
        else:
            return {}


@api.route("/api/v2/videos-count")
class VideosCountEndpoint(Resource):
    def get(self, tags=[]):
        return {"count": Videos.count(tags)}

    def post(self):
        if api.payload and "tags" in api.payload:
            tags = api.payload["tags"]
            return {"count": Videos.count(tags)}
        else:
            return {}


@api.route("/api/v2/index-new-files")
class IndexNewFilesEndpoint(Resource):
    def post(self):
        # set is not JSON serializable, so we have to convert to list
        directories = list(settings.scanned_directories)
        extensions = list(settings.video_extensions)

        backend.tasks.default.rpc_index_new_files.send(
            directories,
            extensions,
        )
        return {"message": "success"}


@api.route("/api/v2/reindex-all")
class ReindexAllEndpoint(Resource):
    def post(self):
        # set is not JSON serializable, so we have to convert to list
        directories = list(settings.scanned_directories)
        extensions = list(settings.video_extensions)

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


@api.route("/api/v2/debug-delete-status")
class DebugDeleteStatusEndpoint(Resource):
    def post(self):
        from backend.api.db import db_status

        db_status.delete_many({})


@api.route("/api/v2/thumbnails/<id>")
class ThumbnailsEndpoint(Resource):
    def get(self, id):
        from bson import ObjectId

        from backend.api.db import fs

        out = fs.get(ObjectId(id))
        return Response(out.read(), mimetype="image/webp")
