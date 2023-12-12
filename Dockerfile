FROM python:3.12.1-alpine3.18 as BUILDER

WORKDIR /workdir
COPY ./builder .
COPY tools.yaml .

RUN pip install -r requirements.txt
RUN python main.py --output-dir=/output --tools-yaml=./tools.yaml

FROM alpine:3.19 as BASE

ENV PATH="/app:${PATH}"
COPY --from=BUILDER /output /app

WORKDIR /workdir
