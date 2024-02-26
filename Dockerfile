FROM python:3.10.13-slim-bookworm as builder
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /usr/src/dormyboba-core
COPY . ./
RUN export POETRY=${HOME}/.local/bin/poetry && \
    ${POETRY} config virtualenvs.in-project true && \
    ${POETRY} install
FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /usr/src/dormyboba-core/ ./
EXPOSE 50051
CMD ["/app/.venv/bin/python3", "-m", "dormyboba_core", "--config-dir", "/config"]
