FROM python:3.8-slim
WORKDIR /app
COPY main.py /app
COPY secrets.py /app
CMD ["python", "/app/main.py"]
