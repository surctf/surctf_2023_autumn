FROM ubuntu:latest

RUN /usr/sbin/useradd --no-create-home -u 1000 ctf

WORKDIR /home/ctf

COPY lucky_number .
COPY flag .

RUN apt-get update
RUN apt-get install -y socat

RUN chown -R root:root /home/ctf

USER ctf

EXPOSE 2371

CMD socat TCP-LISTEN:2371,reuseaddr,fork EXEC:"/home/ctf/lucky_number"
