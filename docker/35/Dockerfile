FROM python:3.5.1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
