FROM alpine:3.19

ENV PATH="/app:${PATH}"

WORKDIR /workdir

# Fix limit color range
ENV TERM="xterm-256color"

# <<INJECT>>

# add xclíp for k9s
# add git for kustomize/kubectl/kubeconform
RUN apk update && \
    apk add --no-cache xclip git

# Print alias commands by default
CMD ["cat", "/app/alias"]
