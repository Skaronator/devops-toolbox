FROM python:3.12.0-alpine3.18 as BUILDER

WORKDIR /workdir
COPY ./builder .
COPY tools.yaml .

RUN pip install -r requirements.txt
RUN python main.py --output-dir=/output --tools-yaml=./tools.yaml

FROM scratch as BASE

WORKDIR /app
COPY --from=BUILDER /output /app
