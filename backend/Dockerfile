FROM python:3.11-alpine

RUN apk add \
    postgresql-dev \
    gcc \
    musl-dev

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]