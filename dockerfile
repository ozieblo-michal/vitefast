FROM --platform=linux/amd64 alpine:3.14

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
    make \
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

ENV RUNNING_IN_CONTAINER=yes

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR 

COPY ./src/backend /src

RUN mkdir /logs

CMD ["poetry", "run", "python", "src/main.py"]
