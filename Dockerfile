# syntax=docker/dockerfile:1

FROM python:3.10.0rc2-alpine3.14 as flask

LABEL maintainer="Lifemapper <github.com/lifemapper>"

RUN addgroup -S lifemapper -g 888 \
 && adduser -S lifemapper -G lifemapper -u 888

RUN mkdir -p /home/lifemapper \
 && chown lifemapper.lifemapper /home/lifemapper

RUN mkdir -p /scratch-path/log \
 && mkdir -p /scratch-path/sessions \
 && chown -R lifemapper.lifemapper /scratch-path

WORKDIR /home/lifemapper
USER lifemapper

COPY --chown=lifemapper:lifemapper ./requirements.txt .

RUN python -m venv venv \
 && venv/bin/pip install --no-cache-dir -r ./requirements.txt

COPY --chown=lifemapper:lifemapper ./flask_app ./flask_app
ENV FLASK_ENV=production
CMD venv/bin/python -m gunicorn -w 4 --bind 0.0.0.0:5000 ${FLASK_APP}



FROM flask as dev-flask

ENV FLASK_ENV=development
CMD venv/bin/python -m ${FLASK_MANAGE} run --host=0.0.0.0
