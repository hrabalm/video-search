FROM tensorflow/tensorflow:2.7 as base

FROM tensorflow/tensorflow:2.7-gpu as base_gpu

WORKDIR /app

COPY . .

RUN python -m pip install pipenv

RUN pipenv install

ENTRYPOINT [ "python", "main.py" ]
