FROM python:3.12.11

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    g++ \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app .

CMD [ "python", "main.py" ]