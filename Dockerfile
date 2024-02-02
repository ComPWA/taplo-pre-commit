FROM ubuntu:22.04

RUN apt-get update \
   && apt-get install -y \
   curl \
   git \
   pkg-config \
   python3-pip \
   && apt-get autoclean -y \
   && apt-get autoremove -y \
   && rm -rf /var/lib/apt/lists/*

# https://github.com/pre-commit/pre-commit/issues/2823
RUN python3 -m pip install pre-commit!=3.2.0

WORKDIR /project

COPY .pre-commit-config.yaml .
RUN git init . && pre-commit install-hooks
