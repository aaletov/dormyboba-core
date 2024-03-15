FROM python:3.10.13-slim-bookworm as builder
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /usr/src/dormyboba-core
COPY dormyboba_core ./dormyboba_core
COPY pyproject.toml poetry.lock ./
RUN export POETRY=${HOME}/.local/bin/poetry && \
    ${POETRY} config virtualenvs.in-project true && \
    ${POETRY} install
FROM python:3.10.13-slim-bookworm
WORKDIR /app
ENV CONFIG_DIR /config
RUN apt-get update && apt-get install -y ca-certificates curl
COPY cert/ca.crt /usr/local/share/ca-certificates
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /usr/src/dormyboba-core/ ./
EXPOSE 50051
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=30s \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["/app/.venv/bin/python3", "-m", "dormyboba_core"]
