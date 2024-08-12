# fastapi with flyio Template


## 1. pip install

```
pip install fastapi
pip install uvicorn
```

## 2. flyio setup

- [flyio install](https://fly.io/docs/hands-on/install-flyctl/)
- login flyio
    ```
    fly auth login
    ```
- create fly.toml
    ```
    flyctl launch
    ```

##  3. add dockerfile

- update according to requirement

```
ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## 4. generate requirement

- requirements.txt is reference

## 5. deploy

```
flyctl deploy
```