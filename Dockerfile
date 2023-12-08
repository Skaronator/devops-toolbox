FROM scratch as BASE

WORKDIR /app
COPY ./dist /app
