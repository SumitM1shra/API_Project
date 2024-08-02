FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY . /app

RUN pip install kubernetes prometheus_api_client

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
