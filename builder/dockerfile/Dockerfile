FROM alpine:3.19.0

LABEL org.opencontainers.image.title="devops-toolbox" \
      org.opencontainers.image.source="https://github.com/Skaronator/devops-toolbox" \
      org.opencontainers.image.description="Toolbox that contains all useful DevOps tools for my day to day job." \
      org.opencontainers.image.vendor="Skaronator"

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
