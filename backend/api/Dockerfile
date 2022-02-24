FROM python:3.9

WORKDIR /app
RUN pip install pipenv
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system
COPY . .

EXPOSE 5000

CMD ["pipenv", "run", "flask", "run"]
