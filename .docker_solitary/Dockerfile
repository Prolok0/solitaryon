FROM node

WORKDIR /home/solitaryon

RUN apt update -y && \
	yarn install

ENTRYPOINT tail -f /etc/passwd
