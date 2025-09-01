FROM debian:bookworm-slim

ENV BWS_VER=1.0.0
ARG PB_VERSION=0.28.3

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates

RUN curl -LO "https://github.com/bitwarden/sdk/releases/download/bws-v$BWS_VER/bws-x86_64-unknown-linux-gnu-$BWS_VER.zip" && \
    unzip -o bws-x86_64-unknown-linux-gnu-$BWS_VER.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/bws && \
    rm bws-x86_64-unknown-linux-gnu-$BWS_VER.zip

ADD https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb/

COPY ./pb_migrations /pb/pb_migrations
COPY ./pb_hooks /pb/pb_hooks

EXPOSE 8080
WORKDIR /pb