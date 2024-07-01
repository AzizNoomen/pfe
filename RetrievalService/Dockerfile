FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY main.py .

ENV PYTHONPATH=/app

EXPOSE 8002

CMD ["python", "main.py"]

