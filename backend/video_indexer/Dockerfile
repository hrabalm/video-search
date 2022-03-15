FROM python:3.10

WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install "poetry==1.1.13"
COPY pyproject.toml poetry.lock /app/
# FIXME: productions vs dev dependencies
# --no-interaction --no-ansi
# see: https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
RUN poetry config virtualenvs.create false && poetry install
COPY . .

EXPOSE 5000

CMD ["poetry", "run", "python", "main.py"]
