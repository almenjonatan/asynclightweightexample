FROM python:3.8.1

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry update

COPY betfairstreamer betfairstreamer

ENV PYTHONPATH /app

CMD ["python", "betfairstreamer/server.py"]
