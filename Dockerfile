FROM python:3.12-slim

RUN mkdir -p /app

COPY ./src /app
WORKDIR /app

RUN pip install -U pipenv

RUN pipenv install --deploy

EXPOSE 8080

CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:8080", "app:app"]