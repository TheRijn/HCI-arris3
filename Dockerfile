FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install pipenv gunicorn
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system

COPY . /app/

ENTRYPOINT ["/app/docker-entrypoint.sh"]