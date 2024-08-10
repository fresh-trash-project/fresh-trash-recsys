ARG PYTHON_VERSION=3.11-slim

FROM python:${PYTHON_VERSION}

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9080"]