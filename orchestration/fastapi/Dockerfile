FROM python:3.13@sha256:a6af772cf98267c48c145928cbeb35bd8e89b610acd70f93e3e8ac3e96c92af8 AS base

ENV BWS_VER=1.0.0
ENV POETRY_VERSION=2.1.3

RUN pip install poetry==$POETRY_VERSION && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./
RUN poetry add 'https://download.pytorch.org/whl/cpu-cxx11-abi/torch-2.7.1%2Bcpu.cxx11.abi-cp313-cp313-linux_x86_64.whl#sha256=e8c1dfca352c5e8ce9afa92b0c38165d2ed186d28f777abbe01119d86e53f372' && poetry install --no-root

RUN curl -LO "https://github.com/bitwarden/sdk/releases/download/bws-v$BWS_VER/bws-x86_64-unknown-linux-gnu-$BWS_VER.zip" && \
    unzip -o bws-x86_64-unknown-linux-gnu-$BWS_VER.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/bws && \
    rm bws-x86_64-unknown-linux-gnu-$BWS_VER.zip

COPY ./src /api
COPY ./pyproject.toml /api/

FROM python:3.13-slim@sha256:6544e0e002b40ae0f59bc3618b07c1e48064c4faed3a15ae2fbd2e8f663e8283 AS deploy

ENV HF_HOME=/tmp/huggingface

RUN groupadd -r worker && useradd --no-log-init -r -g worker worker
USER worker

COPY --from=base /api /api
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

WORKDIR /api