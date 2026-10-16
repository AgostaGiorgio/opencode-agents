FROM python:3.10.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY . .
RUN poetry install

EXPOSE __PORT__

CMD ["poetry", "run", "uvicorn", "src.main:app", "--port", "__PORT__", "--host", "0.0.0.0"]
