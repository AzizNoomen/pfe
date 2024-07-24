FROM bitnami/python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY configuration/ configuration/
COPY main.py .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "main.py"]
