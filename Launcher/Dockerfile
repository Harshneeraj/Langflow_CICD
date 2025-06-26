FROM python:3.10-slim

RUN pip install fastapi uvicorn kubernetes

COPY launcher.py /app/launcher.py

WORKDIR /app

CMD ["uvicorn", "launcher:app", "--host", "0.0.0.0", "--port", "8000"]
