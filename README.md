# video-search

Web application that scans video files and tags them using Deep Neural
Networks and basic metadata extraction.

Video files can then be filtered by those tags.

## Setup

Create a copy of `docker-compose.local.example.yml` called i.e. `docker-compose.local.yml` and modify volume mount binds suitably so that they map your multimedia folders into containers' `/data/`. Then run all the services by combining `docker-compose.yml` files with `docker compose`:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.local.yml build
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.local.yml up
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
