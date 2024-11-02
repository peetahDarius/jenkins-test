FROM python:3.11-alpine

RUN apk add \
    postgresql-dev \
    gcc \
    musl-dev

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY requirements.py requirements.py

RUN pip install requirements.txt

COPY . .

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]