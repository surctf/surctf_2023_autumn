FROM python:3.8-slim

WORKDIR  /app

RUN apt update && apt install -y socat

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

RUN chmod +x ./run.sh
CMD ["./run.sh"]