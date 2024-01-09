FROM alpine:3.19

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
    openssl-dev \
    zlib-dev \
    libffi-dev

RUN apk add --no-cache sqlite sqlite-dev
RUN apk add --no-cache build-base

RUN wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tar.xz

RUN tar -xf Python-3.12.0.tar.xz

WORKDIR /Python-3.12.0

RUN ./configure --enable-optimizations
RUN make -j 4
RUN make altinstall

WORKDIR /
RUN rm -rf Python-3.12.0
RUN rm Python-3.12.0.tar.xz
RUN apk del .build-deps

RUN python3.12 --version

RUN ln -sf /usr/local/bin/python3.12 /usr/bin/python \
 && ln -sf /usr/local/bin/python3.12 /usr/bin/python3 \
 && ln -sf /usr/local/bin/pip3.12 /usr/bin/pip \
 && ln -sf /usr/local/bin/pip3.12 /usr/bin/pip3

RUN apk update && apk add openssh-client

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY ./src /src

CMD ["poetry", "run", "python", "src/main.py"]
