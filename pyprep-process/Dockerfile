FROM python:3.12.11

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    g++ \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY /app .

ENV PYTHONPATH=/workspace

CMD [ "python", "main.py" ]