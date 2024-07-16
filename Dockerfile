ARG PYTHON_VERSION=3.10

FROM python:$PYTHON_VERSION as base

ENV ROOT /app
ENV PYTHONPATH "${PYTHONPATH}:/app/src/"

WORKDIR $ROOT

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && apt-get install -y --no-install-recommends apt-utils \
  && apt-get install -y --no-install-recommends libc-dev \
  && apt-get install -y --no-install-recommends gcc \
  && apt-get install -y --no-install-recommends gettext \
  && apt-get install -y --no-install-recommends vim \
  && apt-get update && apt-get install -y zsh \
  && apt-get clean


RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock $ROOT/
RUN poetry install --no-root --no-dev

ADD .config/.env $ROOT/
COPY src $ROOT/src

RUN apt-get update && apt-get install -y zsh

COPY start.sh $ROOT/start.sh
RUN chmod +x $ROOT/start.sh
ENV PATH="$ROOT:$PATH"

CMD ["start.sh"]
