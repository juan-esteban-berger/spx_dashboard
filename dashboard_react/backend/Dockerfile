FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install wheel setuptools && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8081

CMD python manage.py migrate && \
    python manage.py init_token && \
    python manage.py runserver 0.0.0.0:8081
