FROM alpine:3.19.0

ENV PATH="/app:${PATH}"

WORKDIR /workdir

# Fix limit color range
ENV TERM="xterm-256color"

# Print alias commands by default
CMD ["cat", "/app/alias"]

# add xclíp, nano for k9s
# add git for kustomize/kubectl/kubeconform
RUN apk update && \
    apk add --no-cache xclip git nano
