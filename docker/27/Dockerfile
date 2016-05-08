FROM python:2.7
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
