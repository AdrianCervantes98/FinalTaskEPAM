FROM python:3.9

ENV PYTHONUNBUFFERED True

COPY requirements.txt ./

# Install production dependencies.
RUN set -ex; \
    pip install -r requirements.txt; \
    pip install gunicorn

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app