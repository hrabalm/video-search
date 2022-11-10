FROM python:3.10

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends fish && apt-get purge --autoremove && rm -rf /var/lib/apt/lists/*
# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb && dpkg -i cuda-keyring_1.0-1_all.deb && rm cuda-keyring_1.0-1_all.deb && apt-get update && apt-get install -y --no-install-recommends libcudnn8-dev cuda-cudart-11-2 && apt-get purge --autoremove && rm -rf /var/lib/apt/lists/*


RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /app/
# RUN pdm install --prod --no-lock --no-editable
RUN pdm install --dev --no-lock --no-editable

COPY . .

EXPOSE 5000

CMD ["pdm", "run", "api"]
