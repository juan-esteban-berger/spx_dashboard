# app/Dockerfile

FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8081

HEALTHCHECK CMD curl --fail http://localhost:8081/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8081", "--server.address=0.0.0.0"]
