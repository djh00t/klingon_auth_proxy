FROM python:3.8-slim
WORKDIR /app
COPY src/main.py /app
COPY src/secrets.py /app
CMD ["python", "/app/main.py"]
