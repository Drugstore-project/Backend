FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tudo (inclui /app com nosso código FastAPI)
COPY . .

EXPOSE 8000

ENV PYTHONPATH="/app"


# Em dev: --reload; em prod, remova o --reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
