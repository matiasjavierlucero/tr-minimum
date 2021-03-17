FROM python:3.9.1-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        default-libmysqlclient-dev  \
        build-essential  \
        freetds-bin  \
        curl \
    && python -m pip install --no-cache-dir -r /app/requirements.txt \
    && apt-get purge --auto-remove -yqq build-essential default-libmysqlclient-dev \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    libmariadb-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN pip install gunicorn

COPY . /app

ENTRYPOINT ["bash","./gunicorn_starter.sh"]

