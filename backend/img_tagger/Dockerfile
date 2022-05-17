FROM python:3.10
# FROM tensorflow/tensorflow:2.8.0 as base
# FROM tensorflow/tensorflow:2.8.0-gpu as base_gpu
WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install "poetry==1.2.0a2"
COPY pyproject.toml poetry.lock /app/

# FIXME: productions vs dev dependencies
# --no-interaction --no-ansi
# see: https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
RUN poetry config virtualenvs.create false && poetry install
COPY . .

ENTRYPOINT [ "poetry", "run", "python", "main.py" ]
