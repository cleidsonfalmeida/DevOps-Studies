FROM python:3.11-slim

# Evita prompts interativos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc libpq-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]