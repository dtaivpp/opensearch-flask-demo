# DockerFile
ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

RUN apt-get update && \
    apt-get -y install \
        zsh && \
    rm -rf /var/lib/apt/lists/*
