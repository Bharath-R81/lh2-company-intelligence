FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium

COPY app ./app

EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn app.api:app --host 0.0.0.0 --port ${PORT:-8000}"]