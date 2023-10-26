FROM ubuntu:latest

WORKDIR /ctf

COPY escapeme .

RUN apt-get update
RUN apt-get install -y socat

EXPOSE 2370

RUN chmod +x /ctf/escapeme

CMD socat TCP-LISTEN:2370,reuseaddr,fork EXEC:"/ctf/escapeme"
