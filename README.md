# video-search

Web application that scans video files and tags them using Deep Neural
Networks and basic metadata extraction.

Video files can then be filtered by those tags.

## Setup

Using `docker compose`:

```bash
docker compose build && docker compose up
```

Be aware, that the images that are downloaded and built are quite large, around
~8GB and that building images can take quite long when run for the first time.

At the moment, docker files only setup development servers.

## Technology stack

- React + MUI (frontend)
- Flask + Flask-RESTX (backend API)
- Dramatiq (task queue)
- MongoDB
- Tensorflow/Keras

## Tagging

As far as semantic tags go, currently, video keyframes are passed through Keras
EfficientNetV2-B0 and resulting classes with good enough confidence are considered
as tags for the whole videos.

More interesting tagger is planned in the future.

Other than that, there is some support for simple metadata tags extracted from
the video (e.g. codec, resolution, etc...)
