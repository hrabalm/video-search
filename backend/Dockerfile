FROM python:3.10

WORKDIR /app
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb && dpkg -i cuda-keyring_1.0-1_all.deb && rm cuda-keyring_1.0-1_all.deb && apt-get update && apt-get install -y --no-install-recommends libcudnn8-dev cuda-cudart-11-2 && apt-get purge --autoremove && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install "poetry==1.2.0b1"
COPY pyproject.toml poetry.lock /app/
# FIXME: productions vs dev dependencies
# --no-interaction --no-ansi
# see: https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
RUN poetry config virtualenvs.create false && poetry install
COPY . .

EXPOSE 5000

CMD ["poetry", "run", "python", "app.py"]
