FROM ubuntu:latest

WORKDIR /ctf

COPY lottery.py .

RUN apt-get update
RUN apt-get install -y socat
RUN apt-get install -y python3

EXPOSE 2372

RUN chmod +x /ctf/lottery.py

CMD socat TCP-LISTEN:2372,reuseaddr,fork EXEC:"python3 /ctf/lottery.py"
